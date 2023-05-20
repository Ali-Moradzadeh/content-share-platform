from django.core.management.base import BaseCommand, CommandError
from constants.statics import INITIAL_USERS
from accounting.models import User

class Command(BaseCommand):
    help = 'create initial users'

    def handle(self, *args, **kwargs):
        for init_user in INITIAL_USERS:
            User.objects.create_user(**init_user)
        self.stdout.write(f"Successfully Create {len(INITIAL_USERS)} user objects")