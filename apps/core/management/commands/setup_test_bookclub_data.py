from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from apps.accounts.models import User
from apps.core.models import Book, ReadingList, ReadingListVote

def test_user(username, first_name, last_name='Testerson'):
    email = "%s@test.com" % username
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username, email, 'password')
    else:
        user = User.objects.get(username=username)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return user

def create_reading_list(user, title, topic='fiction', description=' ', books=[]):
    rl = ReadingList(
        title=title,
        category=topic,
        description=description,
        creator_user=user,
    )
    rl.save()

    for book_title in books:
        book = Book(
            title=book_title,
            reading_list=rl,
        )
        book.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError('This command must be run with DEBUG=True')
            return

        # Create some test users
        jane = test_user("janetest", "Jane", "Hacker")
        alice = test_user("alicereader", 'Alice', 'Tester')
        bob = test_user("thebestbob", 'Bob', 'Lablob')

        # Create a bunch of reading lists with various titles
        create_reading_list(
            user=jane,
            title='Fantasy books I recently read',
            books=[
                'The Lord of the Rings',
                'Harry Potter and the Prisoner of Azkaban',
                'A Game of Thrones',
                'The Way of Kings',
            ])

        create_reading_list(
            user=alice,
            title='Favorite books on history and geography',
            topic='nonfiction',
            books=[
                'The Storm Before the Storm: The Beginning of the End of the Roman Republic',
                "Fordlandia: The Rise and Fall of Henry Ford's Forgotten Jungle City",
                'City of Quartz: Excavating the Future in Los Angeles',
                'The Empire of Necessity: Slavery, Freedom, and Deception in the New World',
                'The Age of Empire: 1875-1914',
            ])


        create_reading_list(
            user=bob,
            title='Most misinterpreted science-fiction books',
            description='''
                These are great and interesting books, but the interpretations
                vary wildly, especially without the historical context.
            ''',
            books=[
                'Nineteen Eighty-Four',
                "Ender's Game",
                'Starship Troopers',
                'Snowcrash',
                'Slaughterhouse Five',
            ])

        create_reading_list(
            user=bob,
            title='My favorite science fiction books',
            description='No surprises here, but fun nonetheless',
            books=[
                'Dune',
                'The Left Hand of Darkness',
                'The Martian',
                'Foundation',
                'The Time Machine',
                'The War of the Worlds',
                'I, Robot',
                "Hitchhiker's Guide to the Galaxy",
            ])


        create_reading_list(
            user=alice,
            title='Dystopian YA',
            books=[
                'The Hunger Games',
                'Catching Fire',
                'Mockingjay',
                'Divergent',
                'The Maze Runner',
            ])

        create_reading_list(
            user=alice,
            title='My least favorite pop-history books',
            description="""
                These pop-history books have serious issues, yet they are still
                being recommended, I don't get it...
            """,
            topic='nonfiction',
            books=[
                'Guns, Germs, and Steel: The Fates of Human Societies',
                'Better Angels of Our Nature',
                'The Clash of Civilizations and the Remaking of World Order',
                'The History of the Decline of the Roman Empire',
            ])

        create_reading_list(
            user=jane,
            title='My kids LOVE these books',
            books=[
                'The Cat in the Hat',
                'Goodnight Moon',
                'Winnie-thePooh',
                'Where the Wild Things Are',
                'The Little Prince',
                'Green Eggs and Ham',
            ])

