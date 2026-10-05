from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    BloodRequestForm,
    DonationForm,
    DonorProfileForm,
    RegisterForm,
)
from .models import (
    BloodInventory,
    BloodRequest,
    Donation,
    DonorProfile,
)


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------

def home(request):

    inventory = BloodInventory.objects.all()

    inventory_map = {
        item.blood_group: item
        for item in inventory
    }

    blood_groups = [
        "A+",
        "A-",
        "B+",
        "B-",
        "AB+",
        "AB-",
        "O+",
        "O-",
    ]

    for group in blood_groups:

        if group not in inventory_map:
            inventory_map[group] = None

    total_units = (
        inventory.aggregate(
            total=Sum("units_available")
        )["total"]
        or 0
    )

    donor_count = DonorProfile.objects.filter(
        is_donor=True
    ).count()

    return render(
        request,
        "home.html",
        {
            "blood_groups": blood_groups,
            "inventory_map": inventory_map,
            "total_units": total_units,
            "donor_count": donor_count,
        },
    )


# ---------------------------------------------------------
# REGISTER
# ---------------------------------------------------------

def register(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Your account has been created successfully."
            )

            return redirect("dashboard")

    else:

        form = RegisterForm()

    return render(
        request,
        "register.html",
        {
            "form": form
        },
    )


# ---------------------------------------------------------
# USER DASHBOARD
# ---------------------------------------------------------

@login_required
def dashboard(request):

    profile = DonorProfile.objects.filter(
        user=request.user
    ).first()

    if profile:

        donations = Donation.objects.filter(
            donor=profile
        )[:5]

        donation_count = Donation.objects.filter(
            donor=profile
        ).count()

    else:

        donations = []

        donation_count = 0

    requests = BloodRequest.objects.filter(
        requester=request.user
    )[:5]

    request_count = BloodRequest.objects.filter(
        requester=request.user
    ).count()

    return render(
        request,
        "dashboard.html",
        {
            "profile": profile,
            "donations": donations,
            "requests": requests,
            "donation_count": donation_count,
            "request_count": request_count,
        },
    )


# ---------------------------------------------------------
# DONOR PROFILE
# ---------------------------------------------------------

@login_required
def profile(request):

    donor_profile = DonorProfile.objects.filter(
        user=request.user
    ).first()

    if request.method == "POST":

        form = DonorProfileForm(
            request.POST,
            instance=donor_profile
        )

        if form.is_valid():

            profile_obj = form.save(
                commit=False
            )

            profile_obj.user = request.user

            profile_obj.save()

            messages.success(
                request,
                "Your donor profile has been updated."
            )

            return redirect("profile")

    else:

        form = DonorProfileForm(
            instance=donor_profile
        )

    return render(
        request,
        "profile.html",
        {
            "form": form,
            "profile": donor_profile,
        },
    )


# ---------------------------------------------------------
# DONATE BLOOD
# ---------------------------------------------------------

@login_required
def donate_blood(request):

    donor_profile = DonorProfile.objects.filter(
        user=request.user
    ).first()

    # User must create profile first.
    if not donor_profile:

        messages.warning(
            request,
            "Please complete your donor profile before donating blood."
        )

        return redirect("profile")

    # Check whether donor can donate again.
    if not donor_profile.eligible_to_donate:

        messages.error(
            request,
            "You are not currently eligible to donate. "
            "A 90-day gap is required between donations."
        )

        return redirect("dashboard")

    if request.method == "POST":

        form = DonationForm(
            request.POST
        )

        if form.is_valid():

            with transaction.atomic():

                donation = form.save(
                    commit=False
                )

                donation.donor = donor_profile
                # Always use the donor's actual blood group
                donation.blood_group = donor_profile.blood_group

                donation.save()

                # Only completed donations
                # increase blood inventory.
                if donation.status == "Completed":

                    inventory, created = (
                        BloodInventory.objects.get_or_create(
                            blood_group=donation.blood_group
                        )
                    )

                    inventory.units_available += (
                        donation.units
                    )

                    inventory.save()

                    donor_profile.last_donation_date = (
                        donation.donation_date
                    )

                    donor_profile.save(
                        update_fields=[
                            "last_donation_date",
                            "updated_at",
                        ]
                    )

            messages.success(
                request,
                "Donation recorded successfully. "
                "Thank you for helping save lives!"
            )

            return redirect("dashboard")

    else:

        form = DonationForm()

    return render(
        request,
        "donate.html",
        {
            "form": form,
            "profile": donor_profile,
        },
    )


# ---------------------------------------------------------
# REQUEST BLOOD
# ---------------------------------------------------------

@login_required
def request_blood(request):

    if request.method == "POST":

        form = BloodRequestForm(
            request.POST
        )

        if form.is_valid():

            blood_request = form.save(
                commit=False
            )

            blood_request.requester = (
                request.user
            )

            blood_request.save()

            messages.success(
                request,
                "Your blood request has been submitted successfully."
            )

            return redirect(
                "my_requests"
            )

    else:

        form = BloodRequestForm()

    return render(
        request,
        "request_blood.html",
        {
            "form": form
        },
    )


# ---------------------------------------------------------
# MY BLOOD REQUESTS
# ---------------------------------------------------------

@login_required
def my_requests(request):

    requests = BloodRequest.objects.filter(
        requester=request.user
    )

    return render(
        request,
        "my_requests.html",
        {
            "requests": requests
        },
    )


# ---------------------------------------------------------
# BLOOD INVENTORY
# ---------------------------------------------------------

def blood_inventory(request):

    query = request.GET.get(
        "q",
        ""
    ).strip()

    inventory = BloodInventory.objects.all()

    if query:

        inventory = inventory.filter(
            blood_group__icontains=query
        )

    total_units = (
        BloodInventory.objects.aggregate(
            total=Sum("units_available")
        )["total"]
        or 0
    )

    return render(
        request,
        "inventory.html",
        {
            "inventory": inventory,
            "query": query,
            "total_units": total_units,
        },
    )


# ---------------------------------------------------------
# CANCEL BLOOD REQUEST
# ---------------------------------------------------------

@login_required
@transaction.atomic
def cancel_request(
    request,
    request_id
):

    blood_request = get_object_or_404(
        BloodRequest,
        id=request_id,
        requester=request.user,
    )

    if (
        request.method == "POST"
        and blood_request.status == "Pending"
    ):

        blood_request.status = "Rejected"

        blood_request.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        messages.success(
            request,
            "Your blood request has been cancelled."
        )

    return redirect(
        "my_requests"
    )


# ---------------------------------------------------------
# CHANGE PASSWORD
# ---------------------------------------------------------

@login_required
def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            # Keep the user logged in
            # after changing password.
            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                "Your password has been changed successfully."
            )

            return redirect(
                "dashboard"
            )

    else:

        form = PasswordChangeForm(
            request.user
        )

    return render(
        request,
        "change_password.html",
        {
            "form": form
        },
    )