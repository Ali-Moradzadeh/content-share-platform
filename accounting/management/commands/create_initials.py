from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'create "all" initial datas'

    def handle(self, *args, **kwargs):
        self.stdout.write(f"Processing...")
        call_command("create_users")
        call_command("create_private_chats")
        self.stdout.write(f"Successfully Done.")