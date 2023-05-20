from django.core.management.base import BaseCommand, CommandError
from accounting.models import UserProfile
from contents.models import PrivateChat, PrivateChatDetail

class Command(BaseCommand):
    help = 'create initial users'

    def handle(self, *args, **kwargs):
        count = UserProfile.objects.count()
        count *= (count - 1) * 0.5
        prf = UserProfile.objects.all()
        prfs = {frozenset({x, y}) for x in prf for y in prf if x != y}
        for pare in prfs:
            p = PrivateChat.objects.create()
            for x in pare:
                PrivateChatDetail.objects.create(private_chat=p, member=x)
        
        self.stdout.write(f"Successfully Create private chats")