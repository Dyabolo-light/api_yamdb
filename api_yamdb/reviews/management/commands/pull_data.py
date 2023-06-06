import csv
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Genre, Title, User

OUR_DATABASE = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    User: 'users.csv'
}


class Command(BaseCommand):
    help = 'Загружает базы данных из CSV файлов'

#    def add_arguments(self, parser):
#        parser.add_argument('csv_file', nargs='+', type=str)

    def handle(self, *args, **options):

        for model, csv_file in OUR_DATABASE.items():
            path = f'{settings.BASE_DIR}/static/data/{csv_file}'
            with open(path, 'r', encoding='utf-8') as f:
                rows = csv.DictReader(f, delimiter=',', quotechar='"')
                model.objects.bulk_create(model(**row) for row in rows)
            self.stdout.write(
                self.style.SUCCESS(f'Модель {model.__name__} загружена')
            )




#        for csv_file in options['csv_file']:
#            dataReader = csv.reader(open(csv_file), delimiter=',', quotechar='"')
#            for row in dataReader:
#                emp = Employee()

#                self.stdout.write(
#                    'Created employee {} {}'.format(emp.first_name, emp.last_name)
#                )
