# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Movie(models.Model):
    CATEGORY_CHOICES = [
        ('popular', 'Popular'),
        ('new', 'New')
    ]
    
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    actors = models.CharField(max_length=255)
    summary = models.TextField()
    rating = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='popular')  # Add this line

    def __str__(self):
        return self.title
