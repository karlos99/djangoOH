from django.core.management.base import BaseCommand
from students.models import Staff


class Command(BaseCommand):
    help = 'Import staff data from the CSV file in the imports folder'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing staff data before importing',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing staff data...')
            deleted_count = Staff.objects.all().delete()[0]
            self.stdout.write(
                self.style.WARNING(
                    f'Deleted {deleted_count} existing staff records')
            )

        self.stdout.write('Starting staff data import...')

        try:
            result = Staff.import_from_csv()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully processed {result["total"]} staff records:\n'
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
