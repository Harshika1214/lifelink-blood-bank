from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class DonorProfile(models.Model):

    GENDER_CHOICES = [
        ("Female", "Female"),
        ("Male", "Male"),
        ("Other", "Other"),
    ]

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

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="donor_profile"
    )

    full_name = models.CharField(max_length=100)

    blood_group = models.CharField(
        max_length=3,
        choices=BLOOD_GROUP_CHOICES
    )

    age = models.PositiveIntegerField()

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES
    )

    phone = models.CharField(max_length=15)

    address = models.TextField()

    city = models.CharField(
        max_length=80,
        blank=True
    )

    is_donor = models.BooleanField(
        default=True
    )

    last_donation_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return f"{self.full_name} ({self.blood_group})"

    @property
    def eligible_to_donate(self):

        if not self.is_donor:
            return False

        if not self.last_donation_date:
            return True

        next_eligible_date = (
            self.last_donation_date +
            timedelta(days=90)
        )

        return timezone.localdate() >= next_eligible_date


class BloodInventory(models.Model):

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

    blood_group = models.CharField(
        max_length=3,
        choices=BLOOD_GROUP_CHOICES,
        unique=True
    )

    units_available = models.PositiveIntegerField(
        default=0
    )

    minimum_level = models.PositiveIntegerField(
        default=5
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["blood_group"]

    def __str__(self):
        return f"{self.blood_group} - {self.units_available} units"

    @property
    def status(self):

        if self.units_available == 0:
            return "Critical"

        if self.units_available <= self.minimum_level:
            return "Low"

        return "Available"


class Donation(models.Model):

    STATUS_CHOICES = [
        ("Completed", "Completed"),
        ("Pending", "Pending"),
        ("Rejected", "Rejected"),
    ]

    donor = models.ForeignKey(
        DonorProfile,
        on_delete=models.CASCADE,
        related_name="donations"
    )

    blood_group = models.CharField(
        max_length=3
    )

    units = models.PositiveIntegerField(
        default=1
    )

    donation_date = models.DateField(
        default=timezone.localdate
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Completed"
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            "-donation_date",
            "-created_at"
        ]

    def __str__(self):
        return (
            f"{self.donor.full_name} - "
            f"{self.blood_group} - "
            f"{self.units} unit(s)"
        )


class BloodRequest(models.Model):

    PRIORITY_CHOICES = [
        ("Normal", "Normal"),
        ("Urgent", "Urgent"),
        ("Emergency", "Emergency"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Fulfilled", "Fulfilled"),
        ("Rejected", "Rejected"),
    ]

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

    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blood_requests"
    )

    patient_name = models.CharField(
        max_length=100
    )

    blood_group = models.CharField(
        max_length=3,
        choices=BLOOD_GROUP_CHOICES
    )

    units_required = models.PositiveIntegerField(
        default=1
    )

    hospital_name = models.CharField(
        max_length=150
    )

    hospital_city = models.CharField(
        max_length=80
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="Normal"
    )

    required_date = models.DateField()

    contact_phone = models.CharField(
        max_length=15
    )

    reason = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.patient_name} - "
            f"{self.blood_group} - "
            f"{self.status}"
        )