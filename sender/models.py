from django.db import models
from django.db.models.functions import Now
from django_currentuser.db.models import CurrentUserField
from django.conf import settings
from django.core.mail import send_mail
from smtplib import SMTPException

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
    send_start = models.DateTimeField(verbose_name="Дата и время первой отправки")
    send_stop = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    status = models.CharField(max_length=9, verbose_name="Тема", default='Создана')

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="mailings",
        verbose_name="Сообщение",
    )

    clients = models.ManyToManyField(Client, verbose_name="Клиенты")

    class Meta:
        ordering = ["-id"]



    def send(self):
        attempt = Attempt()
        attempt.mailing = self
        message = self.message

        recipients = [client.email for client in self.clients.all()]

        try:
            send_mail(message.topic, message.text, settings.EMAIL_HOST_USER, recipients, fail_silently=False)
        except SMTPException as e:
            print("--------------- failure -------------------------")
            print(f"type of exception: {type(e)}")

            attempt.server_response = str(e)
            if hasattr(e, 'smtp_code'):
                attempt.server_response = e.smtp_code + ' : ' + e.strerror
            print(attempt.server_response)
        else:
            attempt.is_successful = True
        finally:
            attempt.save()


class Attempt(models.Model):
    """
    модель попытки рассылки.
    Попытка рассылки — это запись о каждой попытке отправки сообщения по рассылке.
    Она содержит информацию о том, была ли попытка успешной, когда она произошла и какой ответ вернул почтовый сервер.
    """
    date_time = models.DateTimeField(verbose_name="Дата и время попытки рассылки", auto_now_add=True)
    is_successful = models.BooleanField(verbose_name="Статус попытки", default=False)
    server_response = models.CharField(max_length=1000, verbose_name="Ответ сервера", blank=True)

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="Рассылка",
    )



