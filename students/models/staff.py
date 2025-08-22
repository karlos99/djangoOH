from django.db import models
import csv
import os
from django.conf import settings


class Staff(models.Model):
    staff_key = models.IntegerField(primary_key=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        db_table = 'staff'
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @classmethod
    def import_from_csv(cls):
        """
        Import staff data from the CSV file in the imports folder
        """
        csv_file_path = os.path.join(settings.BASE_DIR, 'imports', 'staff.csv')

        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"CSV file not found at {csv_file_path}")

        imported_count = 0
        updated_count = 0

        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                staff_key = int(row['staff_key'])

                # Handle empty email values
                email = row['email'].strip() if row['email'].strip() else None

                staff, created = cls.objects.get_or_create(
                    staff_key=staff_key,
                    defaults={
                        'last_name': row['last_name'],
                        'first_name': row['first_name'],
                        'email': email,
                    }
                )

                if created:
                    imported_count += 1
                else:
                    # Update existing record if needed
                    staff.last_name = row['last_name']
                    staff.first_name = row['first_name']
                    staff.email = email
                    staff.save()
                    updated_count += 1

        return {
            'imported': imported_count,
            'updated': updated_count,
            'total': imported_count + updated_count
        }
