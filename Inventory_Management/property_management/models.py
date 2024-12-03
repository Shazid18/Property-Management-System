from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils.timezone import now
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

# Define the upload function outside of any model
def upload_accommodation_image(instance, filename):
    return f'accommodations/{instance.accommodation.id}/{filename}'

class Location(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=100, null=False, blank=False)
    center = models.PointField(geography=True)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children'
    )
    location_type = models.CharField(max_length=20)
    country_code = models.CharField(max_length=2)
    state_abbr = models.CharField(max_length=3, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Accommodation(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    feed = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=100, null=False, blank=False)
    country_code = models.CharField(max_length=2, null=False, blank=False)
    bedroom_count = models.PositiveIntegerField(blank=True, null=True)
    review_score = models.DecimalField(
        max_digits=3, decimal_places=1, default=0.0)
    usd_rate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    center = models.PointField(geography=True)
    images = ArrayField(
        models.CharField(max_length=300),
        blank=True,
        default=list,
    )
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    amenities = models.JSONField(blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # If the user field is not already set and the user is logged in
        if not self.user and hasattr(self, 'user'):
            if self.user is None:
                # If the user is logged in and is not a superuser, assign them
                from django.contrib.auth import get_user_model
                current_user = get_user_model()
                if current_user.is_authenticated and not current_user.is_superuser:
                    self.user = current_user

        super().save(*args, **kwargs)


# models.py
class AccommodationImage(models.Model):
    accommodation = models.ForeignKey(
        Accommodation,
        related_name="accommodation_images",
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to=upload_accommodation_image)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Append the image URL to the accommodation's images field
        if self.image and self.accommodation:
            if self.accommodation.images is None:
                self.accommodation.images = []  # Initialize the images array if it's None
            self.accommodation.images.append(self.image.url)
            self.accommodation.save()

    def __str__(self):
        return f"Image for {self.accommodation.title}"



class LocalizeAccommodation(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(
        Accommodation, on_delete=models.CASCADE, related_name="localizations")
    language = models.CharField(max_length=2)
    description = models.TextField(blank=True, null=True)
    policy = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Localization for {self.property.title} ({self.language})"
