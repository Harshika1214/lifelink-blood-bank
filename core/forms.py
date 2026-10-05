from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import BloodRequest, Donation, DonorProfile


BLOOD_GROUP_CHOICES = [
    ("A+", "A+"),
    ("A-", "A-"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
    ("O+", "O+"),
    ("O-", "O-"),
]


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter your email"
            }
        )
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

    def save(self, commit=True):

        user = super().save(commit=False)

        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


class DonorProfileForm(forms.ModelForm):

    class Meta:
        model = DonorProfile

        fields = [
            "full_name",
            "blood_group",
            "age",
            "gender",
            "phone",
            "address",
            "city",
            "is_donor",
            "last_donation_date",
        ]

        widgets = {

            "blood_group": forms.Select(
                choices=BLOOD_GROUP_CHOICES
            ),

            "age": forms.NumberInput(
                attrs={
                    "min": 18,
                    "max": 65,
                    "placeholder": "Enter your age"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "maxlength": 15,
                    "placeholder": "Enter phone number"
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Enter your address"
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "placeholder": "Enter your city"
                }
            ),

            "last_donation_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),
        }

    def clean_age(self):

        age = self.cleaned_data["age"]

        if age < 18 or age > 65:
            raise forms.ValidationError(
                "Donor age must be between 18 and 65."
            )

        return age


class DonationForm(forms.ModelForm):

    class Meta:
        model = Donation

        fields = [
            "blood_group",
            "units",
            "donation_date",
            "notes",
        ]

        widgets = {

            "blood_group": forms.Select(
                choices=BLOOD_GROUP_CHOICES
            ),

            "units": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 5,
                    "placeholder": "Number of units"
                }
            ),

            "donation_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Optional notes"
                }
            ),
        }

    def clean_units(self):

        units = self.cleaned_data["units"]

        if units < 1 or units > 5:
            raise forms.ValidationError(
                "Units must be between 1 and 5."
            )

        return units


class BloodRequestForm(forms.ModelForm):

    class Meta:
        model = BloodRequest

        fields = [
            "patient_name",
            "blood_group",
            "units_required",
            "hospital_name",
            "hospital_city",
            "priority",
            "required_date",
            "contact_phone",
            "reason",
        ]

        widgets = {

            "blood_group": forms.Select(
                choices=BLOOD_GROUP_CHOICES
            ),

            "units_required": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 20,
                    "placeholder": "Units required"
                }
            ),

            "required_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "contact_phone": forms.TextInput(
                attrs={
                    "maxlength": 15,
                    "placeholder": "Contact phone number"
                }
            ),

            "reason": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Explain why blood is required"
                }
            ),
        }

    def clean_units_required(self):

        units = self.cleaned_data["units_required"]

        if units < 1 or units > 20:
            raise forms.ValidationError(
                "Units must be between 1 and 20."
            )

        return units