from django.shortcuts import redirect

def get_book_cover_url_from_api(title, size='S'):
    '''
    Using the Open Library API, get the URL to the image of the first search
    result's book cover, silences all errors (including 404s).

    >>> url = get_book_cover_url_from_api('Mockingjay', size='M')
    >>> url
    'http://covers.openlibrary.org/b/id/7460251-M.jpg'
    '''
    try:
        import requests
        response = requests.get(f'http://openlibrary.org/search.json?title={title}&limit=1')
        data = response.json()
        cover_id = data['docs'][0]['cover_i']
        url = f'http://covers.openlibrary.org/b/id/{cover_id}-{size}.jpg'
    except Exception as e:
        print('Error trying to access API:', str(e))
        return ''
    return url


def redirect_back(request):
    '''
    A simple trick to redirect back to the previous page
    '''
    return redirect(request.META.get('HTTP_REFERER', '/'))

