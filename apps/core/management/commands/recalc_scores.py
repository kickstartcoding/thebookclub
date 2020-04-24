from django.core.management.base import BaseCommand

from apps.core.models import ReadingList

class Command(BaseCommand):
    def handle(self, *args, **options):
        all_lists = list(ReadingList.objects.all())
        scores = []
        print('----- RAW SCORES -----------')
        for rl in all_lists:
            rl.recalculate_popularity()
            scores.append(rl.score)
            print(f'{rl} | score: {rl.score} | views: {rl.views} | votes: {rl.vote_points}')


        print('----- NORMALIZED SCORES (%) -----------')
        # Calculate and display normalized values
        highest = max(scores)
        lowest = min(scores)
        all_lists.sort(key=lambda rl: -rl.score)
        for rl in all_lists:
            norm = (rl.score - lowest) / (highest - lowest)
            norm_percent = round(norm * 99)
            print(f'%{norm_percent:02} {rl}')




