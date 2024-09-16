import json
from django.core.management.base import BaseCommand
from city.models import City

class Command(BaseCommand):
    help = 'Load cities from a JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file containing city data')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        with open(json_file, 'r') as file:
            data = json.load(file)
            for item in data:
                City.objects.update_or_create(
                    name=item['city'],
                    defaults={
                        'latitude': item.get('lat'),
                        'longitude': item.get('lng')
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded cities from JSON file'))
