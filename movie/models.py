from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    genres = models.CharField(max_length=255, default='Unknown')
    movie_id = models.IntegerField(unique=True)
    overview = models.TextField()
    poster_path = models.URLField()
    release_date = models.DateField(default='2000-01-01')
    runtime = models.IntegerField(default=0)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
    def get_poster_url(self):
        return f'https://image.tmdb.org/t/p/w500{self.poster_path}'


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.movie.title} in cart of {self.cart.user.username}"
