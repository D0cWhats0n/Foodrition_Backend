from django.core.management.base import BaseCommand, CommandError
from foodrition_api.models import Food
from os.path import isfile
import csv
import pandas as pd
import numpy as np


class Command(BaseCommand):
    help = 'Initialises the food database using a .csv file.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        try:
            # Use pandas because parser and dtype are handled more optimal
            df = pd.read_csv(options['file_path'], delimiter=";", 
                             dtype={'Shrt_Desc': str, 'Water_g': np.float64, 
                                    'Energ_Kcal': np.float64, 'Protein_(g)': np.float64,
                                    'Lipid_Tot_(g)': np.float64, 'Ash_(g)': np.float64,
                                    'Carbohydrt_(g)': np.float64})

            for iter_row in df.iterrows():
                row = iter_row[1]
                _, created = Food.objects.get_or_create(
                    name=row['Shrt_Desc'],
                    water_g=row['Water_(g)'],
                    energy_kcal=row['Energ_Kcal'],
                    protein_g=row['Protein_(g)'],
                    lipid_g=row['Lipid_Tot_(g)'],
                    ash_g=row['Ash_(g)'],
                    carbohydrt_g=row['Carbohydrt_(g)']
                    )
            self.stdout.write(self.style.SUCCESS("Succesfully initialized food table from file."))
        except:
            self.stdout.write(self.style.ERROR("Could not initialize food table from file:"))
            raise
