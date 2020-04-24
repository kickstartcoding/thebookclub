from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify


from apps.core import helpers
from apps.core.models import Book, ReadingList, ReadingListVote

@receiver(pre_save, sender=Book)
def update_cover_url(sender, instance, *args, **kwargs):
    '''
    Whenever a book is about to be saved, update it's information from the Open
    Library API
    '''
    book = instance # renaming for convenience
    url = helpers.get_book_cover_url_from_api(book.title)
    book.cover_url = url


@receiver(pre_save, sender=ReadingList)
def update_reading_list_slug(sender, instance, *args, **kwargs):
    '''
    Whenever a ReadingList is about to be saved, ensure that it's slug is
    updated
    '''
    instance.slug = slugify(instance.title)


@receiver(post_save, sender=ReadingList)
def vote_for_own_reading_list(sender, instance, created, *args, **kwargs):
    '''
    Whenever a ReadingList gets first created, cause the creator to
    automatically vote for it
    '''
    if not created:
        return  # Only trigger this when first created

    reading_list = instance # renaming for convenience
    # Create a vote by the user for this reading list
    ReadingListVote.objects.create(
        user=reading_list.creator_user,
        reading_list=reading_list,
        points=1,
    )

    # Now, let's recalculate the score of the reading list
    reading_list.recalculate_popularity()

