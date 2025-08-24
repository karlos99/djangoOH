from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Staff, Student, Course, Enrollment

# Create your views here.


@login_required
def dashboard(request):
    """
    Main dashboard that redirects to appropriate view based on user type
    """
    user_profile = request.user.profile

    if user_profile.user_type == 'STAFF':
        return redirect('staff_dashboard')
    elif user_profile.user_type == 'STUDENT':
        return redirect('student_dashboard')
    else:
        # For users without a specific role yet
        return render(request, 'students/unknown_role.html')


@login_required
def staff_dashboard(request):
    """
    Staff view showing courses taught and enrolled students
    """
    user_profile = request.user.profile

    if user_profile.user_type != 'STAFF':
        return redirect('dashboard')

    staff = user_profile.staff

    # Get courses taught by this staff member
    courses = {}

    # Group enrollments by course and period
    enrollments = Enrollment.objects.filter(staff_key=staff.staff_key)

    for enrollment in enrollments:
        course_key = enrollment.course_key
        period = enrollment.c_period

        # Get the actual course object
        try:
            course = Course.objects.get(course_key=course_key)
            course_name = course.course_name
        except Course.DoesNotExist:
            course_name = f"Unknown Course ({course_key})"

        # Create dict structure if it doesn't exist yet
        if course_key not in courses:
            courses[course_key] = {
                'name': course_name,
                'periods': {}
            }

        if period not in courses[course_key]['periods']:
            courses[course_key]['periods'][period] = []

        # Get student info
        try:
            student = Student.objects.get(
                stu_annual_key=enrollment.stu_annual_key)
            courses[course_key]['periods'][period].append(student)
        except Student.DoesNotExist:
            # Handle missing student
            pass

    context = {
        'staff': staff,
        'courses': courses
    }

    return render(request, 'students/staff_dashboard.html', context)


@login_required
def student_dashboard(request):
    """
    Student view showing enrolled courses
    """
    user_profile = request.user.profile

    if user_profile.user_type != 'STUDENT':
        return redirect('dashboard')

    student = user_profile.student

    # Get enrollments for this student
    enrollments = Enrollment.objects.filter(
        stu_annual_key=student.stu_annual_key)

    courses = []
    for enrollment in enrollments:
        try:
            course = Course.objects.get(course_key=enrollment.course_key)

            # Get teacher info
            teacher = None
            try:
                teacher = Staff.objects.get(staff_key=enrollment.staff_key)
            except Staff.DoesNotExist:
                pass

            courses.append({
                'course': course,
                'period': enrollment.c_period,
                'teacher': teacher
            })
        except Course.DoesNotExist:
            # Handle missing course
            pass

    context = {
        'student': student,
        'courses': courses
    }

    return render(request, 'students/student_dashboard.html', context)
