from django.db import models
import csv
import os
from django.conf import settings


class Course(models.Model):
    course_key = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'course'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.course_name

    @classmethod
    def import_from_csv(cls):
        """
        Import course data from the CSV file in the imports folder
        """
        csv_file_path = os.path.join(
            settings.BASE_DIR, 'imports', 'courses.csv')

        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"CSV file not found at {csv_file_path}")

        imported_count = 0
        updated_count = 0

        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                course_key = int(row['course_key'])

                course, created = cls.objects.get_or_create(
                    course_key=course_key,
                    defaults={
                        'course_name': row['course_name'],
                    }
                )

                if created:
                    imported_count += 1
                else:
                    # Update existing record if needed
                    course.course_name = row['course_name']
                    course.save()
                    updated_count += 1

        return {
            'imported': imported_count,
            'updated': updated_count,
            'total': imported_count + updated_count
        }
