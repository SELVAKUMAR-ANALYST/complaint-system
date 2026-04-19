from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Manager'),
        ('USER', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def is_admin(self):
        return self.role == 'ADMIN'
    
    def is_manager(self):
        return self.role == 'MANAGER'
    
    def is_user(self):
        return self.role == 'USER'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Complaint(models.Model):
    CATEGORY_CHOICES = (
        ('IT', 'IT Support'),
        ('HR', 'HR Department'),
        ('FACILITY', 'Facility Management'),
        ('OTHER', 'Other'),
    )
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    )
    SLA_DAYS = 3  # Overdue after 3 days

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_complaints')
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    reopen_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_overdue(self):
        if self.status == 'RESOLVED':
            return False
        return (timezone.now() - self.created_at).days >= self.SLA_DAYS

    @property
    def days_open(self):
        return (timezone.now() - self.created_at).days

    def __str__(self):
        return self.title

class ComplaintRemark(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='remarks')
    remark = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status_at_remark = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Remark by {self.added_by.username} on {self.complaint.title}"

class ComplaintRating(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]
    complaint = models.OneToOneField(Complaint, on_delete=models.CASCADE, related_name='rating')
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=RATING_CHOICES)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stars}⭐ by {self.rated_by.username} on {self.complaint.title}"
