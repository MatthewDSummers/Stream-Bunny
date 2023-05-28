from django.db import models
import re
import bcrypt
from datetime import datetime,timedelta

class Manager(models.Manager):
    def registerValidator(self,postData):
        errors = {}
        email_already_exists = User.objects.filter(email=postData['email'])
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) <2:
            errors['first_name'] = "*First name should be at least 2 characters"
        if len(postData['last_name']) <2:
            errors['last_name'] = "*Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "*Must use valid email address"
        if len(email_already_exists) > 0:
            errors['email_already_exists'] = "*Email already exists" 
        if len(postData['password']) <8:
            errors['password'] = "*Password must be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "*Confirm password does not match password"
        if postData['birthday']:
            now = datetime.now()
            birthday = datetime.strptime(postData['birthday'],"%Y-%m-%d")
            minimum_age = timedelta(days=4848)
            if now - birthday < minimum_age and birthday < now:
                errors['birthday2'] = "*Must be at least 13 years old"
            if birthday > now:
                errors['birthday1'] = "*Birthday must be in the past"
        else:
                errors['birthday3'] = "*Birthday required"
        return errors
    def loginValidator(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        user = User.objects.filter(email=postData['login_email'])
        if not EMAIL_REGEX.match(postData['login_email']):
            errors['login_email'] = "*Must use valid email address"
        elif not user:
            errors['user_not_found'] = "*User not found"
        else:
            user = user[0]
            if not bcrypt.checkpw(postData['login_password'].encode(),user.password.encode()):
                errors['bad_password'] = "*Password does not match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthday = models.DateField()
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    about = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Manager()

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

class Image(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    user = models.ForeignKey(User, related_name="images", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)