import json
from django.core.management.base import BaseCommand
from property_management.models import Location

class Command(BaseCommand):
    help = "Generate a sitemap.json file for all country locations, including states and cities."

    def handle(self, *args, **kwargs):
        sitemap = []

        # Fetch all country-level locations
        countries = Location.objects.filter(location_type="country").order_by("title")

        for country in countries:
            country_entry = {
                country.title: country.country_code.lower(),
                "states": []
            }

            # Fetch state-level locations under the country
            states = Location.objects.filter(parent=country).order_by("title")

            for state in states:
                state_entry = {
                    state.title: f"{country.country_code.lower()}/{state.title.lower().replace(' ', '-')}",
                    "cities": []
                }

                # Fetch city-level locations under the state
                cities = Location.objects.filter(parent=state).order_by("title")

                for city in cities:
                    city_entry = {
                        city.title: f"{country.country_code.lower()}/{state.title.lower().replace(' ', '-')}/{city.title.lower().replace(' ', '-')}"
                    }
                    state_entry["cities"].append(city_entry)

                country_entry["states"].append(state_entry)

            sitemap.append(country_entry)

        # Write to sitemap.json
        with open("sitemap.json", "w") as f:
            json.dump(sitemap, f, indent=2)

        self.stdout.write(self.style.SUCCESS("sitemap.json generated successfully!"))
