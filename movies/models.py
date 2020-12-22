from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Movie(models.Model):
    name = models.CharField(max_length=150, verbose_name='movie name')
    description = models.TextField(verbose_name='movie description')
    image = models.CharField(max_length=100, verbose_name='movie image')
    release_date = models.DateTimeField(verbose_name='adding time')
    playing_now = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_image_path(self):
        return 'https://image.tmdb.org/t/p/w185_and_h278_bestv2/' + self.image

    def get_comments(self):
        return Comment.objects.filter(movie_id=self.id)

    def get_average_ratings(self):
        ratings = Comment.objects.filter(movie_id=self.id)
        sum = 0
        for rating in ratings:
            sum += rating.rating
        return sum / len(ratings) if len(ratings) > 0 else 0


class Comment(models.Model):
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
