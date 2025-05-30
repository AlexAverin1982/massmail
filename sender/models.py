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

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name



class Message(models.Model):
    """
    модель сообщения в рассылке
    """
    topic = models.CharField(max_length=150, verbose_name="Тема")
    text = models.TextField(max_length=5000, verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')


    class Meta:
        ordering = ["updated_at", "topic"]

    def __str__(self):
        return self.topic

class Mailing(models.Model):
    """
    модель рассылки сообщения списку получателей
    """
    send_start = models.DateTimeField(verbose_name="Дата и время первой отправки", blank=True)
    send_stop = models.DateTimeField(verbose_name="Дата и время окончания отправки", blank=True)
    status = models.CharField(max_length=9, verbose_name="Тема", default='Создана')

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="mailings",
        verbose_name = "Сообщение",
    )

    clients = models.ManyToManyField(Client)

    class Meta:
        ordering = ["-id"]
