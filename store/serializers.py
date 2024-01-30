from rest_framework.serializers import ModelSerializer
from store.models import Book, UserBookRelation
from rest_framework import serializers


class BookSerializer(ModelSerializer):
    likes_count = serializers.SerializerMethodField()  # case without annotations
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author_name', 'likes_count', 'annotated_likes', 'rating')

    # case without annotations
    @staticmethod
    def get_likes_count(instance):
        return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')
