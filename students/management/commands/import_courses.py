from django.core.management.base import BaseCommand
from students.models import Course


class Command(BaseCommand):
    help = 'Import course data from the CSV file in the imports folder'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing course data before importing',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing course data...')
            deleted_count = Course.objects.all().delete()[0]
            self.stdout.write(
                self.style.WARNING(
                    f'Deleted {deleted_count} existing course records')
            )

        self.stdout.write('Starting course data import...')

        try:
            result = Course.import_from_csv()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully processed {result["total"]} course records:\n'
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
