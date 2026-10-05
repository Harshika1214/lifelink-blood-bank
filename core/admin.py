from django.contrib import admin, messages
from django.db import transaction

from .models import (
    BloodInventory,
    BloodRequest,
    Donation,
    DonorProfile,
)


@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "blood_group",
        "age",
        "gender",
        "phone",
        "city",
        "is_donor",
        "last_donation_date",
    )

    list_filter = (
        "blood_group",
        "gender",
        "is_donor",
        "city",
    )

    search_fields = (
        "full_name",
        "phone",
        "city",
        "user__username",
    )


@admin.register(BloodInventory)
class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = (
        "blood_group",
        "units_available",
        "minimum_level",
        "status",
        "updated_at",
    )

    list_filter = (
        "blood_group",
    )

    search_fields = (
        "blood_group",
    )


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = (
        "donor",
        "blood_group",
        "units",
        "donation_date",
        "status",
        "created_at",
    )

    list_filter = (
        "blood_group",
        "status",
        "donation_date",
    )

    search_fields = (
        "donor__full_name",
        "donor__user__username",
    )


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = (
        "patient_name",
        "blood_group",
        "units_required",
        "hospital_name",
        "hospital_city",
        "priority",
        "status",
        "required_date",
        "created_at",
    )

    list_filter = (
        "blood_group",
        "priority",
        "status",
        "hospital_city",
    )

    search_fields = (
        "patient_name",
        "hospital_name",
        "hospital_city",
        "requester__username",
    )

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        old_status = None

        if change:
            old_obj = BloodRequest.objects.select_for_update().get(
                pk=obj.pk
            )
            old_status = old_obj.status

        # When a request becomes Fulfilled,
        # remove the required blood units from inventory.
        if obj.status == "Fulfilled" and old_status != "Fulfilled":

            inventory = BloodInventory.objects.select_for_update().filter(
                blood_group=obj.blood_group
            ).first()

            if not inventory:
                messages.error(
                    request,
                    f"No inventory exists for {obj.blood_group}."
                )
                return

            if inventory.units_available < obj.units_required:
                messages.error(
                    request,
                    f"Not enough {obj.blood_group} blood available. "
                    f"Available: {inventory.units_available} unit(s), "
                    f"Required: {obj.units_required} unit(s)."
                )
                return

            inventory.units_available -= obj.units_required
            inventory.save()

            messages.success(
                request,
                f"{obj.units_required} unit(s) of "
                f"{obj.blood_group} deducted from inventory."
            )

        # If an already fulfilled request is changed back,
        # return its units to inventory.
        elif (
            old_status == "Fulfilled"
            and obj.status != "Fulfilled"
        ):
            inventory = BloodInventory.objects.select_for_update().filter(
                blood_group=obj.blood_group
            ).first()

            if inventory:
                inventory.units_available += obj.units_required
                inventory.save()

                messages.info(
                    request,
                    f"{obj.units_required} unit(s) of "
                    f"{obj.blood_group} returned to inventory."
                )

        super().save_model(request, obj, form, change)