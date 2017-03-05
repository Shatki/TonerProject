import threading

_local_storage = threading.local()


class CurrentRequestMiddleware(object):
    def process_request(self, request):
        _local_storage.request = request


def get_current_request():
    return getattr(_local_storage, "request", None)


def get_current_user():
    request = get_current_request()
    if request is None:
        return None
    return getattr(request, "user", None)


"""
Вообще это нарушает логику работы Django. Там предлагается таскать объект Request вручную, и, да, делать
Client.objects.filter(user=request.user). Если это делается много раз, можно ведь и в функцию оформить:

# models.py
...
def own_clients(request):
    return Client.objects.filter(user=request.user)
...

И, соответственно, пользоваться:

# views.py
from .models import ..., own_clients
...
    ... = own_clients(request).all()

С другой стороны, в принципе, сделать копию request локальной для потока:

# middleware.py

import threading

_local_storage = threading.local()

class CurrentRequestMiddleware(object):
    def process_request(self, request):
        _local_storage.request = request

def get_current_request():
    return getattr(_local_storage, "request", None)

def get_current_user():
    request = get_current_request()
    if request is None:
        return None
    return getattr(request, "user", None)

В settings.py добавить в MIDDLEWARE_CLASSES этот CurrentRequestMiddleware и далее использовать, как и у Вас:

# models.py

from django.db import models
from .middleware import get_current_user

class OwnManager(models.Manager):
    def get_queryset(self):
        qs = super(OwnManager, self).get_queryset()
        return qs.filter(user=get_current_user())

class Client(models.Model):
    ...

    own_objects = OwnManager()

Но все это будет работать до тех пор, пока не поменяется внутреннее устройство фреймворка, а гарантий,
 что на каждый запрос создается отдельный поток никто не давал (хотя по факту это, вроде бы, и так).
 Например, я бы не поручился за работоспособность этого при использовании совместно с django-gevent.
"""
