from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from property_management.models import Accommodation, AccommodationImage, LocalizeAccommodation, Location


class Command(BaseCommand):
    help = 'Create Property Owners group and assign permissions'

    def handle(self, *args, **kwargs):
        # Create Property Owners group if it doesn't exist
        group_name = 'Property Owners'
        property_owners_group, created = Group.objects.get_or_create(name=group_name)

        if created:
            self.stdout.write(f'Created group: {group_name}')
        else:
            self.stdout.write(f'Group already exists: {group_name}')

        # Assign permissions for Location
        self.assign_permissions(Location, property_owners_group)

        # Assign permissions for Accommodation
        self.assign_permissions(Accommodation, property_owners_group)

        # Assign permissions for AccommodationImage
        self.assign_permissions(AccommodationImage, property_owners_group)

        # Assign permissions for LocalizeAccommodation
        self.assign_permissions(LocalizeAccommodation, property_owners_group)

        self.stdout.write(self.style.SUCCESS(
            f'Assigned permissions for related models to the {group_name} group.'))

    def assign_permissions(self, model, group):
        content_type = ContentType.objects.get_for_model(model)
        permissions = Permission.objects.filter(content_type=content_type)

        for perm in permissions:
            group.permissions.add(perm)
