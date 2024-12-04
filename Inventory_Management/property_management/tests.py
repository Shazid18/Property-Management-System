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
        self.assertContains(response, "Hello, World!")

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


# Admin Test


class AdminPermissionTest(TestCase):

    def setUp(self):
        # Create a superuser
        self.superuser = User.objects.create_superuser(
            username='superuser',
            password='password',
            email='superuser@example.com'
        )

        # Create a normal user
        self.user = User.objects.create_user(
            username='user',
            password='password',
            email='user@example.com'
        )

        # Create a "Property Owners" group
        self.group = Group.objects.create(name="Property Owners")
        self.user.groups.add(self.group)

        # Create a location and accommodation instance
        self.location = Location.objects.create(
            id='LOC1',
            title='Test Location',
            location_type='city',
            country_code='US',
            state_abbr='NY',
            city='New York',
            center=Point(0, 0)
        )

        self.accommodation = Accommodation.objects.create(
            id='ACC1',
            title='Test Accommodation',
            country_code='US',
            location=self.location,
            user=self.user,
            center=Point(1, 1),
            published=True
        )

    def test_superuser_can_add_location(self):
        # Log in as superuser and test Location model add permission
        self.client.login(username='superuser', password='password')
        response = self.client.get(
            reverse('admin:property_management_location_add'))
        self.assertEqual(response.status_code, 200)

    # def test_normal_user_cannot_add_location(self):
    #     # Log in as normal user and test Location model add permission
    #     self.client.login(username='user', password='password')
    #     response = self.client.get(
    #         reverse('admin:property_management_location_add'))
    #     self.assertEqual(response.status_code, 403)

    def test_superuser_can_view_and_change_accommodation(self):
        # Log in as superuser and test Accommodation model view and change permission
        self.client.login(username='superuser', password='password')
        response = self.client.get(reverse(
            'admin:property_management_accommodation_change', args=[self.accommodation.id]))
        self.assertEqual(response.status_code, 200)

    # def test_user_can_view_and_change_their_accommodation(self):
    #     # Log in as the user and test that they can view and change their accommodation
    #     self.client.login(username='user', password='password')
    #     response = self.client.get(reverse(
    #         'admin:property_management_accommodation_change', args=[self.accommodation.id]))
    #     self.assertEqual(response.status_code, 200)

    # def test_user_cannot_view_others_accommodation(self):
    #     # Create another user and try to access accommodation owned by another user
    #     another_user = User.objects.create_user(
    #         username='another_user',
    #         password='password',
    #         email='another_user@example.com'
    #     )
    #     accommodation = Accommodation.objects.create(
    #         id='ACC2',
    #         title='Another Accommodation',
    #         country_code='US',
    #         location=self.location,
    #         user=another_user,
    #         center=Point(1, 1),
    #         published=True
    #     )
    #     self.client.login(username='user', password='password')
    #     response = self.client.get(reverse(
    #         'admin:property_management_accommodation_change', args=[accommodation.id]))
    #     self.assertEqual(response.status_code, 403)

#     def test_property_owners_group_can_view_location(self):
#         # Log in as user in the Property Owners group
#         self.client.login(username='user', password='password')
#         response = self.client.get(
#             reverse('admin:property_management_location_changelist'))
#         self.assertEqual(response.status_code, 200)

#     def test_non_superuser_cannot_delete_others_accommodation(self):
#         # Log in as user and try to delete accommodation of another user
#         self.client.login(username='user', password='password')
#         response = self.client.post(
#             reverse('admin:property_management_accommodation_delete',
#                     args=[self.accommodation.id]),
#             {'post': 'yes'}
#         )
#         self.assertEqual(response.status_code, 403)

#     def test_inclusion_of_images_in_accommodation(self):
#         # Test the functionality of adding images to an accommodation via the inline admin
#         image_file = SimpleUploadedFile(
#             'test_image.jpg', b'file_content', content_type='image/jpeg')

#         self.client.login(username='user', password='password')
#         response = self.client.get(reverse(
#             'admin:property_management_accommodation_change', args=[self.accommodation.id]))
#         self.assertContains(response, 'Add another Accommodation image')

#         # Simulate uploading an image
#         response = self.client.post(reverse('admin:property_management_accommodation_change', args=[self.accommodation.id]), {
#             'accommodation_images-TOTAL_FORMS': '0',
#             'accommodation_images-INITIAL_FORMS': '0',
#             'accommodation_images-MIN_NUM_FORMS': '0',
#             'accommodation_images-MAX_NUM_FORMS': '1000',
#             'accommodation_images-0-image': image_file,
#         })
#         # Successfully saved and redirected
#         self.assertEqual(response.status_code, 302)
