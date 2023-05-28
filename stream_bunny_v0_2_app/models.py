from django.db import models
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
from login_app.models import User

def current_year():
    return date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class Movie(models.Model):
    imdb_id = models.CharField(max_length=12, null=True)
    imdb_rating = models.CharField(max_length=3, blank=True, null=True)
    poster_link = models.CharField(max_length=280, blank=True, null=True)
    cast = models.CharField(max_length=280, blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=100, null=True)
    year = models.PositiveSmallIntegerField(
        default=current_year(),
        validators=[MinValueValidator(1878), max_value_current_year],
    )
    director = models.CharField(max_length=100, null=True)
    streaming_on = models.CharField(max_length=100, null=True)
    genres = models.CharField(max_length=100, null=True)
    liked_by = models.ManyToManyField(User, related_name="liked_by")


    def serialize(self):
        return {
            'id':self.id,
            'imdb_id':self.imdb_id,
            'title':self.title,
            'rating':self.imdb_rating,
            'plot':self.plot,
            'poster_link':self.poster_link,
            # 'poster_low':self.poster_low,
            'year':self.year,
            'director':self.director,
            'streaming_on':self.streaming_on,
            'genres':self.genres
        }

    def __str__(self):
        return f'{self.title} - ({self.year})'

# class DiscussionManager(models.Manager):
#     def validator(self,postData):
#         errors = {}
#         if len(postData['discuss']) <2:
#             errors['discussion'] = "*A new post should be at least 1 character"
#         return errors

class Discussion(models.Model):
    user = models.ForeignKey(User, related_name="discussions", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name="discussions", on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # objects = DiscussionManager()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, related_name="comments", on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)