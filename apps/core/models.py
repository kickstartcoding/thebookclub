from django.db import models
from django.utils.timezone import now

# Third Party "taggit" tagging feature
from taggit.managers import TaggableManager

from apps.accounts.models import User

GENRES = [
    ('fiction', 'Adult Fiction'),
    ('nonfiction', 'Adult Non-Fiction'),
    ('children', "Children's Books"),
]

class ReadingList(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    category = models.CharField(max_length=64, choices=GENRES)
    description = models.TextField()

    # Using the third party django-taggit for tag system
    tags = TaggableManager()

    # Time stamp information:
    created = models.DateTimeField(auto_now_add=True) # Add current date
    last_modified = models.DateTimeField(auto_now=True)

    creator_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text='User who created this reading list',
    )

    # Voting and popularity system here:
    votes = models.ManyToManyField(
        User,
        through='ReadingListvote',
        related_name='reading_lists_voted_on',
    )
    vote_points = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def increment_views(self):
        # There is a better way to cause the database to increment a value:
        # self.views += models.F('views') + 1
        # Learn more here:
        # https://docs.djangoproject.com/en/dev/ref/models/expressions/#f-expressions
        self.views += 1
        self.save()

    def recalculate_popularity(self):
        '''
        Recalculate the popularity score using a The Algorithm (TM)
        '''

        # Calculate how old the post is in hours
        age = now() - self.created
        age_in_hours = age.total_seconds() / 60

        # Use "aggregate sum" Django feature to add up all the reading list
        # vote points into a single value in one DB trip
        # https://docs.djangoproject.com/en/dev/ref/models/querysets/#sum
        votes_qs = ReadingListVote.objects.filter(reading_list=self)
        summed_votes_dict = votes_qs.aggregate(models.Sum('points'))
        self.vote_points = summed_votes_dict['points__sum']

        # This is an example of a trending formula, sometimes referred to as
        # "the algorithm", similar to what they might use on a social network
        # Read more here:
        # https://moz.com/blog/reddit-stumbleupon-delicious-and-hacker-news-algorithms-exposed
        score = (
            self.vote_points            # start with vote count
            + self.views * 0.02         # add in 2% of view count
            - (age_in_hours + 2) ** 1.5 # and subtract age + 2 to the 1.5 power
        )

        # Round to the nearest whole value
        self.score = round(score)

        # Save to update score & vote points
        self.save()



class ReadingListVote(models.Model):
    points = models.SmallIntegerField(default=0)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    reading_list = models.ForeignKey(
        ReadingList,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class Book(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    reading_list = models.ForeignKey(
        ReadingList,
        on_delete=models.CASCADE,
    )

    # These are filled in from the Open Library API:
    isbn = models.CharField(max_length=127, null=True, blank=True)
    author = models.CharField(max_length=127, null=True, blank=True)
    cover_url = models.URLField(max_length=127, null=True, blank=True)

    def __str__(self):
        return self.title

