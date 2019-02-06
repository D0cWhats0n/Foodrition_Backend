from django.core.management.base import BaseCommand, CommandError
from foodrition_api.models import Food
from os.path import isfile
import csv


class Command(BaseCommand):
    help = 'Initialises the food database using a .csv file.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        try:
            with open(options['file_path']) as f:
                food_csv_reader = csv.reader(f, delimiter =';')
                next(food_csv_reader, None) # skip header
                
                for row in food_csv_reader:
                    _, created = Food.objects.get_or_create(
                        name=row[1],
                        protein=row[4]
                        )
        except:
            print("Could not initialize food table from file")
            raise
