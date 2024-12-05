from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from property_management.admin import (
    LocationAdmin,
    AccommodationAdmin,
    AccommodationImageAdmin,
    LocalizeAccommodationAdmin
)
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.messages import get_messages
from django.urls import reverse
from django.test import TestCase
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
        self.user = User.objects.create_user(
            username="owner", password="test1234")
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
        self.user = User.objects.create_user(
            username="owner", password="test1234")
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
        # Refresh the instance to get the updated data
        self.accommodation.refresh_from_db()
        # Include /media/ prefix here
        self.assertIn("/media/path/to/image.jpg", self.accommodation.images)


class LocalizeAccommodationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="owner", password="test1234")
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


# Views Test


class ViewsTestCase(TestCase):

    def test_home_view(self):
        """
        Test the home view to ensure it returns the correct response.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_generic.html')

    def test_property_owner_sign_up_get(self):
        """
        Test the GET request for the property owner sign-up page.
        """
        response = self.client.get(reverse('property_owner_sign_up'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'property_owner_sign_up.html')
        self.assertIn('form', response.context)

    def test_property_owner_sign_up_post_valid(self):
        """
        Test the POST request for the property owner sign-up page with valid data.
        """
        valid_data = {
            'username': 'testuser',
            'password1': 'ComplexP@ss123',
            'password2': 'ComplexP@ss123',
            'first_name': 'Test',
            'last_name': 'User',
        }
        response = self.client.post(
            reverse('property_owner_sign_up'), data=valid_data)

        # Check redirection after successful form submission
        self.assertRedirects(response, reverse(
            'property_owner_sign_up_success'))

        # Verify the user was created
        user_exists = User.objects.filter(username='testuser').exists()
        self.assertTrue(user_exists)

        # Verify success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(
            "Your sign-up request has been submitted successfully." in str(message) for message in messages))

    def test_property_owner_sign_up_post_invalid(self):
        """
        Test the POST request for the property owner sign-up page with invalid data.
        """
        invalid_data = {
            'username': '',  # Invalid because username is required
            'password1': 'password123',
            'password2': 'password123',
        }
        response = self.client.post(
            reverse('property_owner_sign_up'), data=invalid_data)

        # Check that it does not redirect and re-renders the form with errors
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'property_owner_sign_up.html')

        # Verify no user was created
        user_exists = User.objects.filter(username='').exists()
        self.assertFalse(user_exists)

        # Verify error message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(
            "There was an error with your sign-up." in str(message) for message in messages))

    def test_property_owner_sign_up_success_view(self):
        """
        Test the property owner sign-up success view.
        """
        response = self.client.get(reverse('property_owner_sign_up_success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'property_owner_sign_up_success.html')