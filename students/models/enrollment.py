from django.db import models
import csv
import os
from django.conf import settings


class Enrollment(models.Model):
    enrollment_key = models.BigIntegerField(primary_key=True)
    stu_annual_key = models.IntegerField()
    staff_key = models.IntegerField()
    course_key = models.IntegerField()
    # Changed to CharField to handle values like "6-7"
    c_period = models.CharField(max_length=10)
    school_id = models.IntegerField()

    class Meta:
        db_table = 'enrollment'
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'

    def __str__(self):
        return f"Enrollment {self.enrollment_key} - Student: {self.stu_annual_key}"

    @classmethod
    def import_from_csv(cls):
        """
        Import enrollment data from the CSV file in the imports folder
        """
        csv_file_path = os.path.join(
            settings.BASE_DIR, 'imports', 'enrollment.csv')

        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"CSV file not found at {csv_file_path}")

        imported_count = 0
        updated_count = 0

        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                enrollment_key = int(row['enrollment_key'])

                enrollment, created = cls.objects.get_or_create(
                    enrollment_key=enrollment_key,
                    defaults={
                        'stu_annual_key': int(row['stu_annual_key']),
                        'staff_key': int(row['staff_key']),
                        'course_key': int(row['course_key']),
                        # No longer converting to int
                        'c_period': row['c_period'],
                        'school_id': int(row['school_id']),
                    }
                )

                if created:
                    imported_count += 1
                else:
                    # Update existing record if needed
                    enrollment.stu_annual_key = int(row['stu_annual_key'])
                    enrollment.staff_key = int(row['staff_key'])
                    enrollment.course_key = int(row['course_key'])
                    # No longer converting to int
                    enrollment.c_period = row['c_period']
                    enrollment.school_id = int(row['school_id'])
                    enrollment.save()
                    updated_count += 1

        return {
            'imported': imported_count,
            'updated': updated_count,
            'total': imported_count + updated_count
        }
