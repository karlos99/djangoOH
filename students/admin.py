from django.contrib import admin
from .models import Student, Staff, Course, Enrollment

# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['stu_annual_key', 'student_name', 'grade',
                    'stu_email', 'current_gpa', 'w_c_gpa', 'school_year']
    list_filter = ['grade', 'school_id', 'school_year']
    search_fields = ['student_name', 'stu_email', 'student_id']
    list_per_page = 50


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['staff_key', 'first_name', 'last_name', 'email']
    search_fields = ['first_name', 'last_name', 'email']
    list_per_page = 50


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_key', 'course_name']
    search_fields = ['course_name']
    list_per_page = 50


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['enrollment_key', 'stu_annual_key',
                    'staff_key', 'course_key', 'c_period', 'school_id']
    list_filter = ['c_period', 'school_id']
    search_fields = ['enrollment_key',
                     'stu_annual_key', 'staff_key', 'course_key']
    list_per_page = 50
