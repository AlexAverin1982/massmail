from logging import Manager

from django.db import models
from django.db.models.functions import Now
from django_currentuser.db.models import CurrentUserField

class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, verbose_name="Ф.И.О.")
    comment = models.TextField(max_length=1000, verbose_name="Комментарий", blank=True)


"""
1. Управление клиентами
Реализовать возможность добавлять, просматривать, редактировать и удалять получателей рассылки (клиентов).

Модель «Получатель рассылки»:

Email (строка, уникальное).
Ф. И. О. (строка).
Комментарий (текст).
"""
# Create your models here.
