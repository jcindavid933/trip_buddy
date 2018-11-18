from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class UserManager(models.Manager):
    def reg_validator(self, postData):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        password_regex = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")
        errors = {}
        if len(postData['first_name']) < 1:
            errors['first_name'] = 'Please enter a valid name!'
        if len(postData['last_name']) < 1:
            errors['last_name'] = 'Please enter a valid name!'
        if not email_regex.match(postData['email']):
            errors['email'] = 'Please enter a valid email address!'
        if not password_regex.match(postData['password']):
            errors['password'] = 'Please enter a valid password with a minimum of eight characters, at least one uppercase letter, one lowercase letter and one number'
        if User.objects.filter(email=postData['email']):
            errors['email_exists'] = 'This email has already been registered'
        elif postData['age'] == '':
            errors['empty'] = 'Please enter an age'
        elif int(postData['age']) < 13:
            errors['age_young'] = 'You must be at least 13 years old to register'
        elif int(postData['age']) > 100:
            errors['age_old'] = 'You too old'
        if postData['password'] != postData['pass_confirm']:
            errors['pass_confirm'] = "Please make sure to type in the same confirmation password"
        return errors

    def age_validator(self, postData):
        errors = {}
        if postData['age'] == '':
            errors['empty'] = 'Please enter an integer'
        elif int(postData['age']) < 13:
            errors['age_young'] = 'You must be at least 13 years old to register'
        elif int(postData['age']) > 100:
            errors['age_old'] = 'You too old'
        return errors
    def email_validator(self, postData):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if not email_regex.match(postData['email']):
            errors['email'] = 'Please enter a valid email address!'
        if User.objects.filter(email=postData['email']):
            errors['email_exists'] = 'This email has already been registered'
        return errors
    def pass_validator(self, postData):
        password_regex = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")
        errors = {}
        if not password_regex.match(postData['password']):
            errors['password'] = 'Please enter a valid password with a minimum of eight characters, at least one uppercase letter, one lowercase letter and one number'
        return errors

    def login_validator(self, postData):
        user = User.objects.filter(email=postData['login_email'])
        errors = {}
        if not user:
            errors['email'] = 'This email address does not exist'
        if user and not bcrypt.checkpw(postData['login_password'].encode(), user[0].password.encode()):
            errors['password'] = 'Invalid password'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    age = models.IntegerField(null=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
