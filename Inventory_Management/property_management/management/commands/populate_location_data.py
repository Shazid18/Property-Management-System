# accommodations/management/commands/populate_location_data.py
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from property_management.models import Location

class Command(BaseCommand):
    help = 'Populate initial location data for countries, states, and cities'

    def handle(self, *args, **kwargs):
        # Define some countries, states, and cities with their coordinates
        countries = [
            {"id": "US", "title": "United States", "center": Point(-98.5795, 39.8283), "country_code": "US", "location_type": "country", "state_abbr": "", "city": ""},
            {"id": "CA", "title": "Canada", "center": Point(-106.3468, 56.1304), "country_code": "CA", "location_type": "country", "state_abbr": "", "city": ""},
            {"id": "GB", "title": "United Kingdom", "center": Point(-3.435973, 55.3781), "country_code": "GB", "location_type": "country", "state_abbr": "", "city": ""},
        ]

        states = [
            {"id": "CA-ON", "title": "Ontario", "center": Point(-81.2546, 51.2538), "country_code": "CA", "location_type": "state", "state_abbr": "ON", "city": "", "parent": "CA"},
            {"id": "US-CA", "title": "California", "center": Point(-119.4179, 36.7783), "country_code": "US", "location_type": "state", "state_abbr": "CA", "city": "", "parent": "US"},
        ]

        cities = [
            {"id": "US-CA-SF", "title": "San Francisco", "center": Point(-122.4194, 37.7749), "country_code": "US", "location_type": "city", "state_abbr": "CA", "city": "San Francisco", "parent": "US-CA"},
            {"id": "CA-ON-TO", "title": "Toronto", "center": Point(-79.3832, 43.6532), "country_code": "CA", "location_type": "city", "state_abbr": "ON", "city": "Toronto", "parent": "CA-ON"},
        ]

        # Insert countries
        for country in countries:
            Location.objects.create(
                id=country["id"],
                title=country["title"],
                center=country["center"],
                country_code=country["country_code"],
                location_type=country["location_type"],
                state_abbr=country["state_abbr"],
                city=country["city"]
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully added country: {country["title"]}'))

        # Insert states (with parent location being the country)
        for state in states:
            parent_location = Location.objects.get(id=state["parent"])
            Location.objects.create(
                id=state["id"],
                title=state["title"],
                center=state["center"],
                country_code=state["country_code"],
                location_type=state["location_type"],
                state_abbr=state["state_abbr"],
                city=state["city"],
                parent=parent_location
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully added state: {state["title"]}'))

        # Insert cities (with parent location being the state)
        for city in cities:
            parent_location = Location.objects.get(id=city["parent"])
            Location.objects.create(
                id=city["id"],
                title=city["title"],
                center=city["center"],
                country_code=city["country_code"],
                location_type=city["location_type"],
                state_abbr=city["state_abbr"],
                city=city["city"],
                parent=parent_location
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully added city: {city["title"]}'))
