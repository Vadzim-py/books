import django_filters
from django.shortcuts import render
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from store.models import Book
from store.serializers import BookSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticated]
    filterset_fields = ['name', 'price']   # filterset_fields in new versions instead of filter_fields
    search_fields = ['name', 'author_name']
    ordering_fields = ['price', 'author_name']


def auth(request):
    return render(request, 'oauth.html')