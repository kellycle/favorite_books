from django.shortcuts import render, redirect
from . models import User, Book
import bcrypt
from django.contrib import messages
from django.contrib.messages import get_messages

# Display
def disp_index(request):
    if 'user_id' in request.session:
        return redirect("/books")
    else:
        return render(request, "index.html")

def disp_books(request):
    if 'user_id' in request.session:
        context = {
            'this_user': User.objects.get(id=request.session['user_id']), 
            'all_books': Book.objects.all(),
            'all_users': User.objects.all(),
        }
        return render(request, "all_books.html", context)
    else:
        return redirect("/")

def disp_book_details(request, book_id):
    context = {
        'this_book': Book.objects.get(id=book_id),
        'all_users': User.objects.all(),
        'this_user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, "book_details.html", context)

# Action
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_pw
        )
        request.session['user_id'] = new_user.id
        return redirect("/books")

def login(request):
    existing_user = User.objects.filter(email=request.POST['email']).first()
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    
    if existing_user is not None:
        if bcrypt.checkpw(request.POST['password'].encode(), existing_user.password.encode()):
            request.session['user_id'] = existing_user.id
            return redirect("/books")
    else:
        return redirect("/")


def process_add(request):
    errors = User.objects.add_book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/books")
    else: 
        new_book = Book.objects.create(
            title = request.POST['title'],
            desc = request.POST['description'],
            uploaded_by = User.objects.get(id=request.session['user_id']),
        )
        this_user = User.objects.get(id=request.session['user_id'])
        this_user.liked_books.add(new_book)
        return redirect("/books")

def process_update(request, book_id):
    this_book = Book.objects.get(id=book_id)
    errors = User.objects.add_book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/books/{book_id}")
    if request.POST['title'] != "":
        this_book.title = request.POST['title']
        this_book.save()
    if request.POST['description'] != "":
        this_book.desc = request.POST['description']
        this_book.save()
    else:
        return redirect(f"/books/{book_id}")
    return redirect(f"/books/{book_id}")

def add_fav(request, book_id):
    this_user = User.objects.get(id=request.session['user_id'])
    this_book = Book.objects.get(id=book_id)

    this_book.users_who_like.add(this_user)
    return redirect(f"/books/{book_id}")

def remove_fav(request, book_id):
    this_user = User.objects.get(id=request.session['user_id'])
    this_book = Book.objects.get(id=book_id)

    this_book.users_who_like.remove(this_user)
    return redirect(f"/books/{book_id}")

def delete(request, book_id):
    this_book = Book.objects.get(id=book_id)
    this_book.delete()
    return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")
