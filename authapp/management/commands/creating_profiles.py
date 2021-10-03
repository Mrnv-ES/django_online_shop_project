from authapp.models import ShopUser, ShopUserProfile
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in ShopUser.objects.filter(shopuserprofile__isnull=True):
            ShopUserProfile.objects.create(user=user)
