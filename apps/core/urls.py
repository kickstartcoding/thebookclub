from django.urls import path

from apps.core import views

urlpatterns = [
    # CRUD views for ReadingLists
    path('', views.reading_list_home, name="home"),
    path('list/<int:list_id>/', views.reading_list_details),
    path('list/create/', views.reading_list_create),
    path('list/delete/<int:list_id>/', views.reading_list_delete),

    # CRUD views for editing Books within ReadingLists
    path('book-create/<int:list_id>/', views.reading_list_create_book),
    path('book-delete/<int:book_id>/', views.reading_list_delete_book),

    # CRUD views for voting on ReadingLists
    path('list/<int:list_id>/vote/up/', views.reading_list_vote_up),
    path('list/<int:list_id>/vote/down/', views.reading_list_vote_down),
]
