from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    class Meta():
        db_table = 'article'
    article_title = models.CharField(max_length=200)
    article_text = models.TextField()
    article_date = models.DateTimeField()
    article_likes = models.IntegerField(default=0)
    def __unicode__(self):
        return self.article_title


class Likes(models.Model):
    class Meta():
        db_table = 'likes'
    likes_article = models.ForeignKey(Article)
    likes_date = models.DateTimeField(auto_now_add=True)
    likes_user = models.ForeignKey(User)


# noinspection PyDocstring
class Comments(models.Model):
    class Meta():
        db_table = 'comments'
    comments_text = models.TextField(verbose_name="Комментарии")
    comments_article = models.ForeignKey(Article)