from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.core.helpers import get_book_cover_url_from_api, redirect_back
from apps.core.models import Book, ReadingList
from apps.core.forms import AddBookForm, AddReadingListForm


def reading_list_home(request):
    # R in CRUD --- READ ReadingLists from database
    # Using order_by('-votes') we'll get it with most votes on top

    reading_lists = ReadingList.objects.all().order_by('-votes').select_related('creator_user')

    context = {
        'all_reading_lists': reading_lists,
    }
    return render(request, 'pages/home.html', context)

def reading_list_details(request, list_id):
    # R in CRUD --- READ a single ReadingList & its books from database
    reading_list_requested = ReadingList.objects.get(id=list_id)
    # SOLUTION:
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
            # C in CRUD --- CREATE reading list in database

            # SOLUTION:
            logged_in_user = request.user
            # print('Current user:', logged_in_user)

            ReadingList.objects.create(
                name=form.cleaned_data['name'],
                topic=form.cleaned_data['topic'],
                # SOLUTION:
                creator_user=logged_in_user,
            )
            return redirect('/')
    else:
        # if a GET  we'll create a blank form
        form = AddReadingListForm()
    context = {
        'form': form,
    }
    return render(request, 'pages/form_page.html', context)


@login_required
def reading_list_delete(request, list_id):
    # D in CRUD --- DELETE reading list from database
    readinglist = ReadingList.objects.get(id=list_id)

    # BONUS: Security
    if readinglist.creator_user == request.user:
        readinglist.delete()

    return redirect('/')


@login_required
def reading_list_create_book(request, list_id):
    # C in CRUD --- CREATE books in database
    reading_list_requested = ReadingList.objects.get(id=list_id)

    # BONUS SOLUTION:
    # Prevent users who are not the requested user from accessing this
    if reading_list_requested.creator_user != request.user:
        return redirect_back(request)

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = AddBookForm(request.POST)
        if form.is_valid():

            url = get_book_cover_url_from_api(form.cleaned_data['title'])

            Book.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                # SOLUTION:
                reading_list=reading_list_requested,
                cover_url=url,
            )
            # Redirect back to the reading list we were at
            return redirect('/list/' + str(reading_list_requested.id) + '/')
    else:
        # if a GET  we'll create a blank form
        form = AddBookForm()
    context = {
        'form': form,
    }
    return render(request, 'pages/form_page.html', context)


@login_required
def reading_list_delete_book(request, book_id):
    # D in CRUD, increase the votes count
    book = Book.objects.get(id=book_id)

    # BONUS SOLUTION: Security
    if book.reading_list.creator_user == request.user:
        book.delete()

    return redirect_back(request)

@login_required
def reading_list_vote_up(request, list_id):
    # U in CRUD, increase the votes count
    reading_list = ReadingList.objects.get(id=list_id)

    # BONUS SOLUTION:
    # Get the currently logged in user
    logged_in_user = request.user
    user_who_voted = reading_list.users_who_voted.filter(id=logged_in_user.id)
    if not user_who_voted.exists():
        print('can vote')
        reading_list.votes = reading_list.votes + 1
        # Record that this user has already voted on this reading list
        reading_list.users_who_voted.add(logged_in_user)
        reading_list.save()

    return redirect_back(request)

@login_required
def reading_list_vote_down(request, list_id):
    # U in CRUD, decrease the votes count
    reading_list = ReadingList.objects.get(id=list_id)

    # BONUS SOLUTION:
    logged_in_user = request.user
    user_who_voted = reading_list.users_who_voted.filter(id=logged_in_user.id)
    if not user_who_voted.exists():
        print('can vote')
        reading_list.votes = reading_list.votes - 1
        # Record that this user has already voted on this reading list
        reading_list.users_who_voted.add(logged_in_user)
        reading_list.save()
    return redirect_back(request)

