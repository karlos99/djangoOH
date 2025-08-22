from django.core.management.base import BaseCommand
from students.models import Enrollment


class Command(BaseCommand):
    help = 'Import enrollment data from the CSV file in the imports folder'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing enrollment data before importing',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing enrollment data...')
            deleted_count = Enrollment.objects.all().delete()[0]
            self.stdout.write(
                self.style.WARNING(
                    f'Deleted {deleted_count} existing enrollment records')
            )

        self.stdout.write('Starting enrollment data import...')

        try:
            result = Enrollment.import_from_csv()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully processed {result["total"]} enrollment records:\n'
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
