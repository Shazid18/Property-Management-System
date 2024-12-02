# from django.contrib import admin
# from .models import Location, Accommodation, AccommodationImage, LocalizeAccommodation


# @admin.register(Location)
# class LocationAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'location_type',
#                     'country_code', 'state_abbr', 'city')
#     search_fields = ('title', 'country_code', 'state_abbr', 'city')


# @admin.register(Accommodation)
# class AccommodationAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'country_code',
#                     'bedroom_count', 'review_score', 'published')
#     search_fields = ('title', 'country_code')
#     list_filter = ('published',)
#     # readonly_fields = ('images',)



# @admin.register(AccommodationImage)
# class AccommodationImageAdmin(admin.ModelAdmin):
#     list_display = ('id', 'accommodation', 'image', 'uploaded_at')
#     search_fields = ('accommodation__title',)


# @admin.register(LocalizeAccommodation)
# class LocalizeAccommodationAdmin(admin.ModelAdmin):
#     list_display = ('id', 'property', 'language')
#     search_fields = ('language',)



from django.contrib import admin
from .models import Location, Accommodation, AccommodationImage, LocalizeAccommodation
from django.forms import BaseInlineFormSet


# Inline formset for handling multiple images
class AccommodationImageInline(admin.TabularInline):  # Inherit from TabularInline
    model = AccommodationImage
    extra = 1  # Number of empty forms to display initially


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location_type',
                    'country_code', 'state_abbr', 'city')
    search_fields = ('title', 'country_code', 'state_abbr', 'city')


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'country_code',
                    'bedroom_count', 'review_score', 'published')
    search_fields = ('title', 'country_code')
    list_filter = ('published',)
    inlines = [AccommodationImageInline]  # Add Accommodation images inline form

    # Optional: Add a method to display image URLs (if needed in list view)
    def image_urls(self, obj):
        return ", ".join(obj.images)  # Join image URLs in a single string
    image_urls.short_description = 'Image URLs'  # Add column header


@admin.register(AccommodationImage)
class AccommodationImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'accommodation', 'image', 'uploaded_at')
    search_fields = ('accommodation__title',)
    readonly_fields = ('image', 'uploaded_at')  # Make image field readonly


@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'language')
    search_fields = ('language',)
