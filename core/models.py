from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

# ----------------------------
# User Model
# ----------------------------

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('vendor', 'Vendor'),
        ('producer', 'Producer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

# ----------------------------
# Producer Model
# ----------------------------

class Producer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    fssai_license = models.CharField(max_length=20)
    contact_info = models.TextField()
    flagged_review_count = models.IntegerField(default=0)
    reported_to_govt = models.BooleanField(default=False)

# ----------------------------
# Vendor Model
# ----------------------------

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    street_location = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.user.username}"

# ----------------------------
# Ratings + Complaint Flag
# ----------------------------

class Rating(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    review = models.TextField()
    is_safety_concern = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# ----------------------------
# Vendor Group Chat (Forum)
# ----------------------------

class VendorGroupChatMessage(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vendor.user.username}: {self.message[:30]}..."

# ----------------------------
# Private Chat
# ----------------------------

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"
