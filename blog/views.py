# -*- coding: utf-8 -*-
from blog.models import Article, Comment, Like
from django.shortcuts import render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from blog.forms import CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from django.contrib import auth
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.

def articles(request, page_number=1):
    all_articles = Article.objects.all()
    current_page = Paginator(all_articles, 2)
    args = {}
    args.update(csrf(request))
    args['articles'] = current_page.page(page_number)
    args['username'] = auth.get_user(request).username
    args['form'] = UserCreationForm()
    return render_to_response('articles.html', args)


def article(request, article_id=1):
    comment_form = CommentForm
    args = {}
    args.update(csrf(request))
    args['article'] = Article.objects.get(id=article_id)
    args['comments'] = Comment.objects.filter(comment_article_id=article_id)
    args['form'] = comment_form
    args['username'] = auth.get_user(request).username
    return render_to_response('article.html', args)



@login_required()
def addlike(request, article_id):
    # пока обязательно проверяем
    if request.method == "GET":
            # article_id приходит через GET запрос
            # article_id = request.GET['article_id']
            article = Article.objects.get(id=article_id)  # подхватываем статью из базы
            user = request.user
            try:
                user_liked = Like.objects.get(like_user=user,
                                              like_article=article_id)  # подхватываем лайки к этой статье
            except ObjectDoesNotExist:
                user_liked = None

            if user_liked:
                user_liked.delete()

                article.article_likes -= 1  # Likes.objects.filter(likes_article_id=article_id).count()
                article.save()
            else:
                user_liked = Like(like_article=article)
                article.article_likes += 1
                user_liked.likes_user = user
                article.save()
                user_liked.save()
                return HttpResponse(article.article_likes, content_type='text/html')
                #return redirect(return_path)
                # except ObjectDoesNotExist:
                # raise Http404
    #Лайков к этой статье вообще нет, сразу выходим
    return HttpResponse(0, content_type='text/html')



@login_required()
def addcomment(request, article_id):
    return_path = request.META.get('HTTP_REFERER', '/')
    if request.POST and ("pause" not in request.session):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comment_article = Article.objects.get(id=article_id)
            form.save()
            request.session.set_expiry(60) #ограничение ввода комментариев
            request.session['pause'] = True
    return redirect(return_path)
