from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.core.helpers import redirect_back
from apps.core.models import Book, ReadingList, ReadingListVote
from apps.core.forms import AddBookForm, AddReadingListForm
from apps.core import signals

def reading_list_home(request):
    # R in CRUD --- READ ReadingLists from database

    reading_lists = ReadingList.objects.all().select_related('creator_user')

    # Using order_by('-score') we'll get it with most votes on top
    reading_lists = reading_lists.order_by('-score')

    if request.user.is_authenticated:
        # If the user is logged in, get the votes that the user did for the
        # reading lists in question
        relevant_votes = ReadingListVote.objects.filter(
            reading_list__in=reading_lists,
            user=request.user,
        )
    else:
        relevant_votes = []


    if 'sort_by' in request.GET:
        if request.GET['sort_by'] == 'new':
            reading_lists = reading_lists.order_by('-created')
        elif request.GET['sort_by'] == 'votes':
            reading_lists = reading_lists.order_by('-vote_points')
    else:
        reading_lists = reading_lists.order_by('-score')


    context = {
        'reading_lists': reading_lists,
        'relevant_votes': relevant_votes,
    }
    return render(request, 'pages/home.html', context)

def reading_list_details(request, list_slug):
    # R in CRUD --- READ a single ReadingList & its books from database
    reading_list_requested = ReadingList.objects.get(slug=list_slug)

    # Count views of pages for determining trending
    reading_list_requested.increment_views()

    books = Book.objects.filter(reading_list=reading_list_requested)
    context = {
        'reading_list': reading_list_requested,
        'all_books': books,
    }
    return render(request, 'pages/details.html', context)

@login_required
def reading_list_create(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = AddReadingListForm(request.POST)
        if form.is_valid():
            # If we had omitted commit=False, then the user would not have been
            # properly set-up
            instance = form.save(commit=False)
            instance.creator_user = request.user
            instance.save()
            return redirect('/')
    else:
        # if a GET  we'll create a blank form
        form = AddReadingListForm()
    context = {
        'form': form,
        'form_title': 'New book list',
    }
    return render(request, 'pages/form_page.html', context)


@login_required
def reading_list_delete(request, list_id):
    # D in CRUD --- DELETE reading list from database
    readinglist = ReadingList.objects.get(id=list_id)

    if readinglist.creator_user != request.user:
        return redirect('/')

    readinglist.delete()
    return redirect('/')


@login_required
def reading_list_create_book(request, list_id):
    # C in CRUD --- CREATE books in database
    reading_list_requested = ReadingList.objects.get(id=list_id)

    # Prevent users who are not the requested user from accessing this
    if reading_list_requested.creator_user != request.user:
        return redirect_back(request)

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = AddBookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.reading_list = reading_list_requested
            book.save()

            # Redirect back to the reading list we were at
            return redirect('/list/' + str(reading_list_requested.id) + '/')
    else:
        # if a GET  we'll create a blank form
        form = AddBookForm()
    context = {
        'form': form,
        'form_title': 'Add book',
    }
    return render(request, 'pages/form_page.html', context)


@login_required
def reading_list_delete_book(request, book_id):
    # D in CRUD, increase the votes count
    book = Book.objects.get(id=book_id)

    if book.reading_list.creator_user == request.user:
        book.delete()

    return redirect_back(request)

@login_required
def reading_list_vote(request, list_id, up_or_down):
    # If "up" was specified, then we want 1 as the voting points, otherwise -1
    if up_or_down == 'up':
        vote_value = 1
    else:
        vote_value = -1
    reading_list = ReadingList.objects.get(id=list_id)

    # If there is already a vote, update_or_creaate will update that from the
    # database with the "points" value.  If none exists, then it will create a
    # new one. See:
    # https://docs.djangoproject.com/en/3.0/ref/models/querysets/#update-or-create
    ReadingListVote.objects.update_or_create(
        user=request.user,
        reading_list=reading_list,
        defaults={'points': vote_value},
    )

    # Now, let's recalculate the score of the reading list
    reading_list.recalculate_popularity()
    return redirect_back(request)
