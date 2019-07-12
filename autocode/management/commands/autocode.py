from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = 'Create default group, superuser, topics and sectors.'

    def handle(self, *args, **options):
        User = get_user_model()
        admin = User.objects.filter(is_superuser=True).first()
        print(User)
        if not admin:
            admin = User.objects.create_superuser(email='butterflynet@butterfly.com.au',
                                                  username='butterflynet@butterfly.com.au',
                                                  password='But3as2flying',
                                                  first_name='butterfly',
                                                  last_name='butterfly')
        self.stdout.write(self.style.SUCCESS('Superuser and contributor group created.'))
