from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from .models import Location, Accommodation, AccommodationImage, LocalizeAccommodation


# Inline formset for handling multiple images
# Inherit from TabularInline
class AccommodationImageInline(admin.TabularInline):
    model = AccommodationImage
    extra = 1  # Number of empty forms to display initially


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location_type',
                    'country_code', 'state_abbr', 'city')
    search_fields = ('title', 'country_code', 'state_abbr', 'city')

    def has_add_permission(self, request):
        # Allow adding only for superusers
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        # Allow changing only for superusers
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        # Allow deleting only for superusers
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        # Allow viewing for superusers and members of the Property Owners group
        return (
            request.user.is_superuser or 
            request.user.groups.filter(name="Property Owners").exists()
        )


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'country_code', 'bedroom_count', 'review_score', 'published')
    search_fields = ('title', 'country_code')
    list_filter = ('published',)
    inlines = [AccommodationImageInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        # If the user is a superuser, allow them to select a user
        if request.user.is_superuser:
            obj.user = form.cleaned_data.get('user', None)
        else:
            # If not a superuser, automatically set the user to the current logged-in user
            obj.user = request.user

        obj.save()

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        
        # If the user is not a superuser, hide the 'user' field from the form
        if not request.user.is_superuser:
            fields = [field for field in fields if field != 'user']
        return fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Ensure that the 'user' field is read-only for staff and normal users, but editable for superusers.
        """
        if db_field.name == "user" and not request.user.is_superuser:
            kwargs['disabled'] = True  # Disable the 'user' field for staff and normal users
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None or obj.user == request.user:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None or obj.user == request.user:
            return True
        return False


@admin.register(AccommodationImage)
class AccommodationImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'accommodation', 'image', 'uploaded_at')
    search_fields = ('accommodation__title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(accommodation__user=request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None or obj.accommodation.user == request.user:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None or obj.accommodation.user == request.user:
            return True
        return False


@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'language')
    search_fields = ('language',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(property__user=request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None or obj.property.user == request.user:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None or obj.property.user == request.user:
            return True
        return False
