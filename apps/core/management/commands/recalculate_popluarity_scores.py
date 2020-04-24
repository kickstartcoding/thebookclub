from django.core.management.base import BaseCommand

from apps.core.models import ReadingList

class Command(BaseCommand):
    def handle(self, *args, **options):
        all_lists = ReadingList.objects.all():
        for rl in all_lists:
            rl.recalculate_popularity()

