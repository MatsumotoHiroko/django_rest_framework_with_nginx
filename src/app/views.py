import django_filters
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, filters
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from .models import Book, Rate
from .serializer import BookSerializer, RateSerializer

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

class BookViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated|ReadOnly,)
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.none()
    serializer_class = RateSerializer
    
    permission_classes_by_action = {'list': [IsAuthenticated],
                                   'create': [AllowAny]}
    def get_permissions(self):
      try:
        # return permission_classes depending on `action`
        return [permission() for permission in self.permission_classes_by_action[self.action]]
      except KeyError:
        # action is not set return default permission_classes
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        return Rate.objects.filter(book=self.kwargs['book_pk'])

