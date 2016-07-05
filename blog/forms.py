# -*- coding: utf-8 -*-
__autor__ = 'macpro'

from django.forms import ModelForm
from blog.models import Comment

# Форма для оставления комментарий к статьям
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comments_text']
