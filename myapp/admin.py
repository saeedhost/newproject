from django.contrib import admin
from myapp.models import Book, Author

#Custom Action Customization
def mark_published(modeladmin, request, queryset):
    queryset.update(status ='published')
    mark_published.short_description = "Mark Selected Books are published"


# Builtin Customization 
class BookInline(admin.TabularInline):  # You can also use StackedInline instead of TabularInline
    model = Book
    extra = 1

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    inlines = [BookInline]
admin.site.register(Author, AuthorAdmin)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'publish_date', 'price', 'author', 'status')
    search_fields = ('title', 'author__name')
    list_filter = ('id','title', 'publish_date')
    
    actions = [mark_published]