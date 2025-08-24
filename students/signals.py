from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Staff, Student, UserProfile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    When a User is created/updated, create/update their UserProfile
    and try to associate them with Staff or Student based on email
    """
    if created:
        UserProfile.objects.create(user=instance)

    # Try to link with Staff or Student based on email
    staff = None
    student = None

    # Only proceed if email is provided
    if instance.email:
        # Check if email matches a staff member
        try:
            staff = Staff.objects.get(email__iexact=instance.email)
        except Staff.DoesNotExist:
            pass

        # If not staff, check if email matches a student
        if not staff:
            try:
                student = Student.objects.get(stu_email__iexact=instance.email)
            except Student.DoesNotExist:
                pass

    # Update the user's profile
    profile = UserProfile.objects.get_or_create(user=instance)[0]
    profile.staff = staff
    profile.student = student

    # Set user_type based on what was found
    if staff:
        profile.user_type = 'STAFF'
    elif student:
        profile.user_type = 'STUDENT'

    profile.save()
