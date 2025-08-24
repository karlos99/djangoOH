from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
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
                'periods': {},
                'total_students': 0
            }

        if period not in courses[course_key]['periods']:
            courses[course_key]['periods'][period] = []

        # Get student info
        try:
            student = Student.objects.get(
                stu_annual_key=enrollment.stu_annual_key)
            courses[course_key]['periods'][period].append(student)
            courses[course_key]['total_students'] += 1
        except Student.DoesNotExist:
            # Handle missing student
            pass

    # Process the courses to organize them in a structure that's easier to work with in the template
    processed_courses = []
    for course_id, course_data in courses.items():
        # Sort periods
        sorted_periods = []
        for period_id, students in course_data['periods'].items():
            sorted_periods.append({
                'period': period_id,
                'students': students,
                'count': len(students)
            })

        # Sort periods by period ID (ascending)
        sorted_periods.sort(key=lambda x: x['period'])

        processed_courses.append({
            'id': course_id,
            'name': course_data['name'],
            'periods': sorted_periods,
            'total_students': course_data['total_students']
        })

    # Sort courses by total students (descending)
    processed_courses.sort(key=lambda x: x['total_students'], reverse=True)

    # Create a JSON-friendly version for Vue.js
    import json
    courses_json = json.dumps([{
        'id': course['id'],
        'name': course['name'],
        'total_students': course['total_students'],
        'periods': [p['period'] for p in course['periods']]
    } for course in processed_courses])

    context = {
        'staff': staff,
        'courses': processed_courses,
        'courses_json': courses_json
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


@login_required
def load_period_students(request, course_id, period):
    """
    JSON endpoint to load students for a specific course and period
    """
    user_profile = request.user.profile

    if user_profile.user_type != 'STAFF':
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    staff = user_profile.staff

    # Get students for this course and period
    try:
        course = Course.objects.get(course_key=course_id)
        course_name = course.course_name
    except Course.DoesNotExist:
        course_name = f"Unknown Course ({course_id})"

    # Get enrollments for this course and period
    enrollments = Enrollment.objects.filter(
        staff_key=staff.staff_key,
        course_key=course_id,
        c_period=period
    )

    students_data = []
    for enrollment in enrollments:
        try:
            student = Student.objects.get(
                stu_annual_key=enrollment.stu_annual_key)
            students_data.append({
                'id': student.stu_annual_key,
                'name': student.student_name,
                'grade': student.grade,
                'period': enrollment.c_period,
                'gpa': student.current_gpa
            })
        except Student.DoesNotExist:
            pass

    # Sort by student name
    students_data.sort(key=lambda x: x['name'])

    return JsonResponse({
        'course_name': course_name,
        'period': period,
        'students': students_data
    })


@login_required
def student_schedule(request, student_id):
    """
    View for a teacher to see a specific student's complete schedule
    """
    user_profile = request.user.profile

    if user_profile.user_type != 'STAFF':
        return redirect('dashboard')

    # Get the student
    student = get_object_or_404(Student, stu_annual_key=student_id)

    # Get all enrollments for this student
    enrollments = Enrollment.objects.filter(stu_annual_key=student_id)

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

    # Sort courses by period
    courses.sort(key=lambda x: x['period'])

    context = {
        'student': student,
        'courses': courses
    }

    return render(request, 'students/partials/student_schedule.html', context)


@login_required
def course_students(request, course_id):
    """
    API endpoint to get all students for a specific course across all periods
    """
    user_profile = request.user.profile

    if user_profile.user_type != 'STAFF':
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    staff = user_profile.staff

    # Get enrollments for this course
    enrollments = Enrollment.objects.filter(
        staff_key=staff.staff_key,
        course_key=course_id
    )

    students_data = []
    for enrollment in enrollments:
        try:
            student = Student.objects.get(
                stu_annual_key=enrollment.stu_annual_key)
            students_data.append({
                'id': student.stu_annual_key,
                'name': student.student_name,
                'grade': student.grade,
                'period': enrollment.c_period,
                'gpa': student.current_gpa
            })
        except Student.DoesNotExist:
            pass

    # Sort by period, then by last name
    students_data.sort(key=lambda x: (x['period'], x['name']))
    
    # Get course details
    try:
        course = Course.objects.get(course_key=course_id)
        course_name = course.course_name
    except Course.DoesNotExist:
        course_name = f"Unknown Course ({course_id})"

    return JsonResponse({
        'course_name': course_name,
        'students': students_data
    })
