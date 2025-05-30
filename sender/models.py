from django.db import models
from django.db.models.functions import Now
from django_currentuser.db.models import CurrentUserField

class Client(models.Model):
    """
    модель получателя рассылки (клиента)
    """
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, verbose_name="Ф.И.О.")
    comment = models.TextField(max_length=1000, verbose_name="Комментарий", blank=True)




class Message(models.Model):
    """
    модель сообщения в рассылке
    """
    topic = models.CharField(max_length=150, verbose_name="Тема")
    text = models.TextField(max_length=5000, verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
