from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('staff/course/<int:course_id>/period/<str:period>/students/',
         views.load_period_students, name='load_period_students'),
    path('staff/student/<int:student_id>/schedule/',
         views.student_schedule, name='student_schedule'),
    path('students/course/<int:course_id>/students/',
         views.course_students, name='course_students'),
]
