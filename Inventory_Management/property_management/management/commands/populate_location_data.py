from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from property_management.models import Location


class Command(BaseCommand):
    help = 'Populate initial location data for countries, states, and cities'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Run the command without making changes')

    def create_location(self, data, parent=None, dry_run=False):
        """
        Helper function to create a location object.
        :param data: Dictionary containing location data.
        :param parent: Parent location object.
        :param dry_run: If True, no database operations are performed.
        :return: Boolean indicating if the location was created.
        """
        if Location.objects.filter(id=data["id"]).exists():
            self.stdout.write(self.style.WARNING(f'{data["title"]} already exists.'))
            return False

        if dry_run:
            self.stdout.write(self.style.NOTICE(f'[Dry Run] Would create: {data}'))
            return False

        Location.objects.create(
            id=data["id"],
            title=data["title"],
            center=data["center"],
            country_code=data["country_code"],
            location_type=data["location_type"],
            state_abbr=data["state_abbr"],
            city=data["city"],
            parent=parent
        )
        return True

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        # Define some countries, states, and cities with their coordinates
        countries = [
            {"id": "US", "title": "United States", "center": Point(-98.5795, 39.8283),
             "country_code": "US", "location_type": "country", "state_abbr": "", "city": ""},
            {"id": "CA", "title": "Canada", "center": Point(-106.3468, 56.1304),
             "country_code": "CA", "location_type": "country", "state_abbr": "", "city": ""},
            {"id": "GB", "title": "United Kingdom", "center": Point(-3.435973, 55.3781),
             "country_code": "GB", "location_type": "country", "state_abbr": "", "city": ""},
             {"id": "BD", "title": "Bangladesh", "center": Point(90.3563, 23.685),
             "country_code": "BD", "location_type": "country", "state_abbr": "", "city": ""},
        ]

        states = [
            {"id": "CA-ON", "title": "Ontario", "center": Point(-81.2546, 51.2538),
             "country_code": "CA", "location_type": "state", "state_abbr": "ON", "city": "", "parent": "CA"},
            {"id": "US-CA", "title": "California", "center": Point(-119.4179, 36.7783),
             "country_code": "US", "location_type": "state", "state_abbr": "CA", "city": "", "parent": "US"},
            {"id": "BD-DHA", "title": "Dhaka", "center": Point(90.4125, 23.8103),
             "country_code": "BD", "location_type": "state", "state_abbr": "DHA", "city": "", "parent": "BD"},
        ]

        cities = [
            {"id": "US-CA-SF", "title": "San Francisco", "center": Point(-122.4194, 37.7749),
             "country_code": "US", "location_type": "city", "state_abbr": "CA", "city": "San Francisco", "parent": "US-CA"},
            {"id": "CA-ON-TO", "title": "Toronto", "center": Point(-79.3832, 43.6532),
             "country_code": "CA", "location_type": "city", "state_abbr": "ON", "city": "Toronto", "parent": "CA-ON"},
            {"id": "BD-DHA-MI", "title": "Mirpur", "center": Point(90.4125, 23.8103),
             "country_code": "BD", "location_type": "city", "state_abbr": "DHA", "city": "Mirpur", "parent": "BD-DHA"},
        ]

        # Insert countries
        for country in countries:
            if self.create_location(country, dry_run=dry_run):
                self.stdout.write(self.style.SUCCESS(f'Successfully added country: {country["title"]}'))

        # Insert states
        for state in states:
            try:
                parent_location = Location.objects.get(id=state["parent"])
                if self.create_location(state, parent=parent_location, dry_run=dry_run):
                    self.stdout.write(self.style.SUCCESS(f'Successfully added state: {state["title"]}'))
            except Location.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Parent location with ID {state["parent"]} not found for state: {state["title"]}'))

        # Insert cities
        for city in cities:
            try:
                parent_location = Location.objects.get(id=city["parent"])
                if self.create_location(city, parent=parent_location, dry_run=dry_run):
                    self.stdout.write(self.style.SUCCESS(f'Successfully added city: {city["title"]}'))
            except Location.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Parent location with ID {city["parent"]} not found for city: {city["title"]}'))
