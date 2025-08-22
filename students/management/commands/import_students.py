from django.core.management.base import BaseCommand
from students.models import Student


class Command(BaseCommand):
    help = 'Import student data from the CSV file in the imports folder'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing student data before importing',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing student data...')
            deleted_count = Student.objects.all().delete()[0]
            self.stdout.write(
                self.style.WARNING(
                    f'Deleted {deleted_count} existing student records')
            )

        self.stdout.write('Starting student data import...')

        try:
            result = Student.import_from_csv()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully processed {result["total"]} student records:\n'
                    f'  - Imported: {result["imported"]} new records\n'
                    f'  - Updated: {result["updated"]} existing records'
                )
            )
        except FileNotFoundError as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'An error occurred during import: {e}')
            )
