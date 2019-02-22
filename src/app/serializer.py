# coding: utf-8
from rest_framework import serializers

from .models import Book, Rate


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('name', 'price', 'published_at')


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ('value', 'created_at', 'book')

    def create(self, validated_data):    
        book = Book.objects.get(pk=self.context['view'].kwargs['book_pk'])
        return Rate.objects.create(value=self.validated_data["value"], book=book)