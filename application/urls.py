from django.urls import path
from . import views

urlpatterns = [
    # Display
    path('', views.disp_index),
    path('books', views.disp_books),
    path('books/<int:book_id>', views.disp_book_details),
    # Action
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('process_add', views.process_add),
    path('process_update/<int:book_id>', views.process_update),
    path('book/<int:book_id>/destroy', views.delete),
    path('add_fav/<int:book_id>', views.add_fav),
    path('remove_fav/<int:book_id>', views.remove_fav)
]