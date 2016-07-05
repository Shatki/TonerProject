from django.contrib import admin
from blog.models import Article, Comment, Like

class ArticleInline(admin.StackedInline):
    model = Comment
    extra = 2

class ArticleAdmin(admin.ModelAdmin):
    fields = ['article_title', 'article_text', 'article_date']
    search_fields = ['article_title', 'article_text']
    list_display = ['article_date', 'article_title', 'article_likes']
    inlines = [ArticleInline]


# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(Like)
admin.site.register(Comment)
