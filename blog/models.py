from django.db import models
from authentication.models import Account

# Create your models here.
class Article(models.Model):
    class Meta:
        db_table = 'article'
    article_title = models.CharField(max_length=200)
    article_text = models.TextField()
    article_date = models.DateTimeField()
    article_likes = models.IntegerField(default=0)
    def __unicode__(self):
        return self.article_title


class Like(models.Model):
    class Meta:
        db_table = 'like'
    likes_article = models.ForeignKey(Article)
    likes_date = models.DateTimeField(auto_now_add=True)
    likes_user = models.ForeignKey(Account)


# noinspection PyDocstring
class Comment(models.Model):
    class Meta:
        db_table = 'comment'

    comments_text = models.TextField(verbose_name="Комментарий")
    comments_article = models.ForeignKey(Article)
