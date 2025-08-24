from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    USER_TYPES = (
        ('STAFF', 'Staff'),
        ('STUDENT', 'Student'),
        ('ADMIN', 'Administrator'),
        ('UNKNOWN', 'Unknown'),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(
        max_length=10, choices=USER_TYPES, default='UNKNOWN')
    staff = models.OneToOneField(
        'Staff', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_profile')
    student = models.OneToOneField(
        'Student', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_profile')

    def __str__(self):
        return f"{self.user.username} ({self.get_user_type_display()})"

    def save(self, *args, **kwargs):
        # If user_type isn't explicitly set, determine it based on linked models
        if self.staff:
            self.user_type = 'STAFF'
        elif self.student:
            self.user_type = 'STUDENT'
        super().save(*args, **kwargs)
