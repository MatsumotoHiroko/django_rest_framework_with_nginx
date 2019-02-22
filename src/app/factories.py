# -*- coding: utf-8 -*-
import factory
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class TokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Token

    user = factory.SubFactory(UserFactory, user=UserFactory)


