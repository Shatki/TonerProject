from django.db import models
from authentication.models import Account


# Create your models here.
class Article(models.Model):
    class Meta:
        db_table = 'article'
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    article_title = models.CharField(max_length=200)
    article_text = models.TextField()
    article_date = models.DateTimeField()
    article_likes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.article_title


class Like(models.Model):
    class Meta:
        db_table = 'like'
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    likes_article = models.ForeignKey(Article, on_delete=models.CASCADE)
    likes_date = models.DateTimeField(auto_now_add=True)
    likes_user = models.ForeignKey(Account, on_delete=models.CASCADE)


# noinspection PyDocstring
class Comment(models.Model):
    class Meta:
        db_table = 'comment'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    comments_text = models.TextField(verbose_name="Комментарий")
    comments_article = models.ForeignKey(Article, on_delete=models.CASCADE)
