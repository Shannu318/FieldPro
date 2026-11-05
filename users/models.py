from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):

    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        TECHNICIAN = "TECHNICIAN", "Technician"
        MANAGER = "MANAGER", "Manager"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    def __str__(self):
        return self.username

class CustomerProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE, 
        related_name='customerprofile')
    
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# service request model for customers to create service requests and for technicians to manage them
class ServiceRequest(models.Model):

    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        URGENT = "URGENT", "Urgent"

    class Status(models.TextChoices):
        NEW = "NEW", "New"
        ASSIGNED = "ASSIGNED", "Assigned"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="service_requests"
    )

    technician = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="assigned_requests"
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    address = models.TextField()

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.customer.username}"