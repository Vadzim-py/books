from django.contrib import admin
from store.models import Book, UserBookRelation

admin.site.register(Book)


class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(UserBookRelation)
class UserBookRelationAdmin(admin.ModelAdmin):
    pass
