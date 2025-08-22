from django.core.management.base import BaseCommand
from students.models import Student, Staff, Course, Enrollment


class Command(BaseCommand):
    help = 'Import all data from CSV files in the imports folder'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before importing',
        )

    def handle(self, *args, **options):
        models_to_import = [
            ('Course', Course),
            ('Staff', Staff),
            ('Student', Student),
            ('Enrollment', Enrollment),
        ]

        total_imported = 0
        total_updated = 0

        for model_name, model_class in models_to_import:
            if options['clear']:
                self.stdout.write(
                    f'Clearing existing {model_name.lower()} data...')
                deleted_count = model_class.objects.all().delete()[0]
                self.stdout.write(
                    self.style.WARNING(
                        f'Deleted {deleted_count} existing {model_name.lower()} records')
                )

            self.stdout.write(f'Starting {model_name.lower()} data import...')

            try:
                result = model_class.import_from_csv()

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully processed {result["total"]} {model_name.lower()} records:\n'
                        f'  - Imported: {result["imported"]} new records\n'
                        f'  - Updated: {result["updated"]} existing records'
                    )
                )

                total_imported += result["imported"]
                total_updated += result["updated"]

            except FileNotFoundError as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error importing {model_name.lower()}: {e}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'An error occurred during {model_name.lower()} import: {e}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n=== IMPORT SUMMARY ===\n'
                f'Total imported: {total_imported} records\n'
                f'Total updated: {total_updated} records\n'
                f'Grand total: {total_imported + total_updated} records'
            )
        )
