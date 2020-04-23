from django.shortcuts import redirect
import requests

API_URL_PREFIX = 'http://openlibrary.org/search.json?limit=1&title='

def get_book_cover_url_from_api(title, size='S', info=None):
    '''
    Using the Open Library API, get the URL to the image of the first search
    result's book cover, silences all errors (including 404s).

    >>> url = get_book_cover_url_from_api('Mockingjay', size='M')
    >>> url
    'http://covers.openlibrary.org/b/id/7460251-M.jpg'
    '''
    if not info:
        info = get_book_info_from_api(title, size='S')
    url = ''
    if 'cover_i' in info:
        cover_id = info['cover_i']
        url = f'http://covers.openlibrary.org/b/id/{cover_id}-{size}.jpg'
    return url


def get_book_info_from_api(title):
    '''
    Using the Open Library API, get info on the first book.
    '''
    try:
        response = requests.get(API_URL_PREFIX + title)
        data = response.json()
        results = list(data['docs'])
    except Exception as e:
        print('Error trying to access API:', str(e))
        return None
    if len(results) < 1:
        return None
    return results[0]

def redirect_back(request):
    '''
    A simple trick to redirect back to the previous page
    '''
    return redirect(request.META.get('HTTP_REFERER', '/'))

