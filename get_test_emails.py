#!/usr/bin/env python
from students.models import Staff, Student
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()


print("=== SAMPLE STAFF EMAILS ===")
staff_with_emails = Staff.objects.exclude(
    email__isnull=True).exclude(email='')[:5]
if staff_with_emails:
    for staff in staff_with_emails:
        print(
            f"  Staff ID: {staff.staff_key}, Name: {staff.full_name}, Email: {staff.email}")
else:
    print("  No staff with emails found.")
    # Find staff without emails
    staff_without_emails = Staff.objects.all()[:5]
    print("\n  Staff without emails (you can manually assign emails in admin):")
    for staff in staff_without_emails:
        print(f"  Staff ID: {staff.staff_key}, Name: {staff.full_name}")

print("\n=== SAMPLE STUDENT EMAILS ===")
students_with_emails = Student.objects.exclude(
    stu_email__isnull=True).exclude(stu_email='')[:5]
for student in students_with_emails:
    print(
        f"  Student ID: {student.stu_annual_key}, Name: {student.student_name}, Email: {student.stu_email}")

print("\n=== TESTING INSTRUCTIONS ===")
print("1. Go to the admin site: http://127.0.0.1:8000/admin/")
print("2. Create users with matching emails from the samples above")
print("3. Log in at: http://127.0.0.1:8000/login/")
print("4. The system should redirect you to the appropriate dashboard based on your role")
