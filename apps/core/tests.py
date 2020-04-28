from django.test import TestCase

from apps.core.models import ReadingList, Book
from apps.accounts.models import User


class EmptySiteTestCase(TestCase):
    def test_homepage_shows_expected_links(self):
        # Ensures homepage has some expected text, and links to log-in and
        # sign-up
        response = self.client.get('/')
        self.assertContains(response, 'The Book Club')

        # "html=True" is a feature of Django that will tolerate slight
        # differences in HTML (e.g. whitespace, order of attributes)
        login_html = '''
            <a class="btn btn-link text-light" href="/account/login/">
                Already have an account? Log in now.
            </a>
        '''
        self.assertContains(response, login_html, html=True)
        signup_html = '''
            <a class="btn btn-lg btn-secondary" href="/account/signup/">
                Sign-up to get book clubbing!
            </a>
        '''
        self.assertContains(response, signup_html, html=True)

    def test_results_indicates_empty(self):
        response = self.client.get('/')
        self.assertContains(response, 'No reading lists... yet!', html=True)

    def test_signup(self):
        # Simulate the POST request for a sign-up
        self.client.post('/account/signup/', {
            'username': 'testuser',
            'password1': 'g00d_p@55w0rd',
            'password2': 'g00d_p@55w0rd',
            'email': 'testuser@fake.com',
        })

        # Now make sure the account was created and shows expected HTML
        response = self.client.get('/')
        self.assertContains(response, 'Account created successfully. Welcome!', html=True)

        # Ensure the user is logged in & displaying a link to the user's page
        expected_navbar_link = 'href="/account/users/testuser/"'
        self.assertContains(response, expected_navbar_link)


class C5ModelReadingListUnitTestCase(TestCase):
    def setUp(self):
        # Setup is run before every test, and can be used to setup test data.
        # Since this is a "unit test", we won't be using fixtures since that
        # would be overkill -- "small" is the goal here.
        fake_user = User.objects.create_user('testuser')
        self.reading_list = ReadingList.objects.create(
            title='Testing list',
            category='fiction',
            creator_user=fake_user,
        )

    def test_increment_views(self):
        # Ensure the views start at 0
        self.assertEqual(self.reading_list.views, 0)
        # Run function
        self.reading_list.increment_views()
        self.assertEqual(self.reading_list.views, 1)

    def test_get_absolute_url(self):
        url = self.reading_list.get_absolute_url()
        self.assertEqual(url, '/testing-list/')

    def test_str(self):
        # BONUS SOLUTION:
        self.reading_list.title = 'Testing list'
        s = self.reading_list.__str__()
        self.assertEqual(s, 'Testing list')

