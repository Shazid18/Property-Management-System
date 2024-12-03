from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from .models import Location, Accommodation, AccommodationImage, LocalizeAccommodation


class LocationModelTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            id="1",
            title="New York",
            center=Point(-74.006, 40.7128),
            location_type="City",
            country_code="US",
            state_abbr="NY",
            city="New York",
        )

    def test_location_str(self):
        self.assertEqual(str(self.location), "New York")


class AccommodationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="owner", password="test1234")
        self.location = Location.objects.create(
            id="1",
            title="New York",
            center=Point(-74.006, 40.7128),
            location_type="City",
            country_code="US",
            state_abbr="NY",
            city="New York",
        )
        self.accommodation = Accommodation.objects.create(
            id="1",
            title="Luxury Apartment",
            country_code="US",
            bedroom_count=3,
            review_score=4.5,
            usd_rate=150.00,
            center=Point(-74.006, 40.7128),
            location=self.location,
            user=self.user,
            published=True,
        )

    def test_accommodation_str(self):
        self.assertEqual(str(self.accommodation), "Luxury Apartment")

    def test_accommodation_defaults(self):
        self.assertEqual(self.accommodation.feed, 0)
        self.assertEqual(self.accommodation.review_score, 4.5)
        self.assertTrue(self.accommodation.published)


class AccommodationImageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="owner", password="test1234")
        self.location = Location.objects.create(
            id="1",
            title="New York",
            center=Point(-74.006, 40.7128),
            location_type="City",
            country_code="US",
            state_abbr="NY",
            city="New York",
        )
        self.accommodation = Accommodation.objects.create(
            id="1",
            title="Luxury Apartment",
            country_code="US",
            bedroom_count=3,
            review_score=4.5,
            usd_rate=150.00,
            center=Point(-74.006, 40.7128),
            location=self.location,
            user=self.user,
            published=True,
        )

    def test_accommodation_image_save(self):
        # Assuming 'path/to/image.jpg' is the image path you're testing
        image_instance = AccommodationImage.objects.create(
            accommodation=self.accommodation,
            image='path/to/image.jpg'
        )
        self.accommodation.refresh_from_db()  # Refresh the instance to get the updated data
        self.assertIn("/media/path/to/image.jpg", self.accommodation.images)  # Include /media/ prefix here


class LocalizeAccommodationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="owner", password="test1234")
        self.location = Location.objects.create(
            id="1",
            title="New York",
            center=Point(-74.006, 40.7128),
            location_type="City",
            country_code="US",
            state_abbr="NY",
            city="New York",
        )
        self.accommodation = Accommodation.objects.create(
            id="1",
            title="Luxury Apartment",
            country_code="US",
            bedroom_count=3,
            review_score=4.5,
            usd_rate=150.00,
            center=Point(-74.006, 40.7128),
            location=self.location,
            user=self.user,
            published=True,
        )
        self.localization = LocalizeAccommodation.objects.create(
            property=self.accommodation,
            language="en",
            description="A luxurious apartment in NYC",
            policy={"check_in": "2 PM", "check_out": "11 AM"},
        )

    def test_localization_str(self):
        self.assertEqual(
            str(self.localization), "Localization for Luxury Apartment (en)"
        )

    def test_localization_policy(self):
        self.assertEqual(self.localization.policy["check_in"], "2 PM")
        self.assertEqual(self.localization.policy["check_out"], "11 AM")
