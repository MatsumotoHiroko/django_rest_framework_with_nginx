from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Book(models.Model):
    name = models.CharField(max_length=32)
    price = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9999999999)])
    published_at = models.DateTimeField()

class Rate(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank = True, null=True)
    value = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)