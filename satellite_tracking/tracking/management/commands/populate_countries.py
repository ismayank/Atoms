from django.core.management.base import BaseCommand
from tracking.models import LaunchCountry

class Command(BaseCommand):
    help = 'Populate launch countries'

    def handle(self, *args, **kwargs):
        countries = ['USA', 'Russia', 'China', 'India', 'Japan', 'France', 'UK', 'Germany', 'Canada', 'Italy']
        for country in countries:
            LaunchCountry.objects.get_or_create(name=country)
        self.stdout.write(self.style.SUCCESS('Successfully populated launch countries'))
