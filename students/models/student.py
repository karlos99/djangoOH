from django.db import models
import csv
import os
from django.conf import settings


class Student(models.Model):
    stu_annual_key = models.IntegerField(primary_key=True)
    student_id = models.CharField(max_length=20)
    student_name = models.CharField(max_length=255)
    grade = models.IntegerField()
    stu_email = models.EmailField()
    current_gpa = models.DecimalField(
        max_digits=5, decimal_places=4, null=True, blank=True)
    w_c_gpa = models.DecimalField(
        max_digits=5, decimal_places=4, null=True, blank=True)
    school_id = models.IntegerField()
    school_year = models.CharField(max_length=20)

    class Meta:
        db_table = 'student'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.student_name} (Grade {self.grade})"

    @classmethod
    def import_from_csv(cls):
        """
        Import student data from the CSV file in the imports folder
        """
        csv_file_path = os.path.join(
            settings.BASE_DIR, 'imports', 'student.csv')

        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"CSV file not found at {csv_file_path}")

        imported_count = 0
        updated_count = 0

        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                stu_annual_key = int(row['stu_annual_key'])

                # Handle empty GPA values
                current_gpa = None
                if row['current_gpa'].strip():
                    current_gpa = float(row['current_gpa'])

                w_c_gpa = None
                if row['w_c_gpa'].strip():
                    w_c_gpa = float(row['w_c_gpa'])

                student, created = cls.objects.get_or_create(
                    stu_annual_key=stu_annual_key,
                    defaults={
                        'student_id': row['student_id'],
                        'student_name': row['student_name'],
                        'grade': int(row['grade']),
                        'stu_email': row['stu_email'],
                        'current_gpa': current_gpa,
                        'w_c_gpa': w_c_gpa,
                        'school_id': int(row['school_id']),
                        'school_year': row['school_year'],
                    }
                )

                if created:
                    imported_count += 1
                else:
                    # Update existing record if needed
                    student.student_id = row['student_id']
                    student.student_name = row['student_name']
                    student.grade = int(row['grade'])
                    student.stu_email = row['stu_email']
                    student.current_gpa = current_gpa
                    student.w_c_gpa = w_c_gpa
                    student.school_id = int(row['school_id'])
                    student.school_year = row['school_year']
                    student.save()
                    updated_count += 1

        return {
            'imported': imported_count,
            'updated': updated_count,
            'total': imported_count + updated_count
        }
