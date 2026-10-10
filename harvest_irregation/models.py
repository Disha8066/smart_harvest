
from django.db import models
from django.contrib.auth.models import User


# ==========================================
# HARVEST MODEL
# ==========================================

class Harvest(models.Model):

    CROP_CHOICES = [
        ("Rice", "Rice"),
        ("Wheat", "Wheat"),
        ("Corn", "Corn"),
        ("Potato", "Potato"),
        ("Vegetable", "Vegetable"),
        ("Other", "Other"),
    ]

    STATUS_CHOICES = [
        ("Growing", "Growing"),
        ("Ready", "Ready"),
        ("Harvested", "Harvested"),
        ("Stored", "Stored"),
    ]

    farmer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="harvests",
    )

    crop_name = models.CharField(
        max_length=100,
        choices=CROP_CHOICES,
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Harvest quantity in KG",
    )

    harvest_date = models.DateField()

    location = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Growing",
    )

    water_used = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Water used in liters",
    )

    soil_moisture = models.PositiveIntegerField(
        default=50,
        help_text="Soil moisture percentage",
    )

    temperature = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=25,
    )

    humidity = models.PositiveIntegerField(
        default=60,
        help_text="Humidity percentage",
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-harvest_date", "-created_at"]

    def __str__(self):
        return f"{self.crop_name} - {self.quantity} KG"


# ==========================================
# CHAT MESSAGE MODEL
# ==========================================

class ChatMessage(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_chat_messages",
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_chat_messages",
    )

    message = models.TextField(
        max_length=5000,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    is_read = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"


# ==========================================
# FARMER MODEL
# ==========================================

class Farmer(models.Model):

    name = models.CharField(max_length=150)

    email = models.EmailField(blank=True)

    phone = models.CharField(max_length=20)

    location = models.CharField(max_length=200)

    main_crop = models.CharField(
        max_length=100,
        blank=True,
    )

    # Optional link to the farmer's actual login account.
    # Existing Farmer records can remain without a linked account.
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="farmer_profile",
    )

    # The user who registered this farmer's details.
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="registered_farmers",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


# ==========================================
# BUYER MODEL
# ==========================================

class Buyer(models.Model):

    PRODUCT_CHOICES = [
        ("rice", "Rice and grains"),
        ("vegetables", "Vegetables"),
        ("fruits", "Fruits"),
        ("potatoes", "Potatoes"),
        ("other", "Other produce"),
    ]

    name = models.CharField(max_length=150)

    email = models.EmailField(blank=True)

    phone = models.CharField(max_length=20)

    location = models.CharField(
        max_length=200,
        blank=True,
    )

    interested_product = models.CharField(
        max_length=20,
        choices=PRODUCT_CHOICES,
        blank=True,
    )

    notes = models.TextField(blank=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="registered_buyers",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
