from django.db import models

from apps.accounts.models import User

class ReadingList(models.Model):
    name = models.CharField(unique=True, max_length=30)
    topic = models.CharField(max_length=64)
    votes = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True) # Add current date
    last_modified = models.DateTimeField(auto_now=True)

    # SOLUTION:
    creator_user = models.ForeignKey(User, on_delete=models.CASCADE)

    # BONUS SOLUTION:
    users_who_voted = models.ManyToManyField(
        User,
        related_name='reading_lists_voted_on',
    )


class Book(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    cover_url = models.URLField(max_length=127)

    # SOLUTION:
    reading_list = models.ForeignKey(
        ReadingList,
        on_delete=models.CASCADE,
    )

