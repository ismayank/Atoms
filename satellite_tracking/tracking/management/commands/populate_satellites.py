import csv
import requests
from django.core.management.base import BaseCommand
from tracking.models import Satellite, LaunchCountry
from datetime import datetime

class Command(BaseCommand):
    help = 'Populate satellites'

    def handle(self, *args, **kwargs):
        url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=last-30-days&FORMAT=json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.stdout.write(self.style.SUCCESS(f"Response status code: {response.status_code}"))
            self.stdout.write(self.style.SUCCESS(f"Response content: {response.text[:500]}"))
            data = response.json()
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Request error: {e}"))
            return
        except requests.exceptions.JSONDecodeError as e:
            self.stderr.write(self.style.ERROR(f"JSON decode error: {e}"))
            return

        # Assuming the data structure and creating a dummy mapping for country
        country_map = {
            'USA': LaunchCountry.objects.get(name='USA'),
            'Russia': LaunchCountry.objects.get(name='Russia'),
            # Add mappings for other countries accordingly
        }

        if not data:
            self.stderr.write(self.style.ERROR("No data found in the response."))
            return

        count = 0
        filename = 'satellites_data.csv'
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['name', 'international_designator', 'norad_id', 'launch_date', 'decay_date', 'country']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for satellite_data in data:
                country = country_map.get('USA')  # Default to USA for this example
                writer.writerow({
                    'name': satellite_data.get('OBJECT_NAME', 'Unknown'),
                    'international_designator': satellite_data.get('OBJECT_ID', 'Unknown'),
                    'norad_id': satellite_data.get('NORAD_CAT_ID', 0),
                    'launch_date': datetime.strptime(satellite_data.get('LAUNCH_DATE', '1900-01-01'), '%Y-%m-%d'),
                    'decay_date': datetime.strptime(satellite_data.get('DECAY_DATE', '1900-01-01'), '%Y-%m-%d') if satellite_data.get('DECAY_DATE') else None,
                    'country': country.name if country else 'Unknown'
                })
                count += 1
                if count >= 600:
                    break

        self.stdout.write(self.style.SUCCESS(f'Successfully stored data in {filename}, containing {count} satellites'))
