# -*- coding: utf-8 -*-
__autor__ = 'macpro'

from django.forms import ModelForm
from blog.models import Comments

# Форма для оставления комментарий к статьям
class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['comments_text']
