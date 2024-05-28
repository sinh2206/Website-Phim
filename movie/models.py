from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=255)
    overview = models.TextField()
    poster_path = models.CharField(max_length=255)
    runtime = models.IntegerField()
    release_date = models.DateField()
    genres = models.TextField()
    movie_id = models.IntegerField(unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)  # Ensure this line is correct

    def get_poster_url(self):
        return self.poster_path
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie, through='CartItem')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.movie.title} in cart of {self.cart.user.username}"
