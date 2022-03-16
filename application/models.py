from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 2 and len(postData['last_name']) < 2:
            errors['name'] = "First name & last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if User.objects.filter(email = postData['email']).exists() == True:
            errors['email'] = "Account already exists!"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors['password_check'] = "Your passwords don't match"
        if postData['confirm_password'] == "":
            errors['pw_confirm'] = "Passwords should match"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        if postData['email'] == "" or postData['password'] == "":
            errors['invalid'] = "Invalid email and/or password"
        elif User.objects.filter(email = postData['email']).exists() != True:
            errors['email'] = "Account does not exist"
        if User.objects.filter(email = postData['email']).exists() == True:
            existing_user = User.objects.filter(email = postData['email']).first()
            if bcrypt.checkpw(postData['password'].encode(), existing_user.password.encode()) != True:
                errors['invalid'] = "Invalid email and/or password"
        return errors
    
    def add_book_validator(self, postData):
        errors = {}
        if postData['title'] == "":
            errors['title'] = "title is required"
        if len(postData['description']) < 5:
            errors['description'] = "description must be at least 5 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # liked_books = a list of books a given user likes
    # books_uploaded = a list of books uploaded by a given user

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete = models.CASCADE) 
        # the user who uploaded a given book
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
        # a list of users who like a given book