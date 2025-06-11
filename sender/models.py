from django.db import models
# from django.db.models.functions import Now
from django.conf import settings
from django.core.mail import send_mail
from smtplib import SMTPException

from users.models import CustomUser


class Client(models.Model):
    """
    модель получателя рассылки (клиента)
    """
    email = models.EmailField()
    full_name = models.CharField(max_length=150, verbose_name="Ф.И.О.")
    comment = models.TextField(max_length=1000, verbose_name="Комментарий", blank=True)

    owner = models.ForeignKey(CustomUser, editable=False, on_delete=models.SET_NULL, related_name='Клиенты',
                              verbose_name='Владелец', blank=True, null=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "клиенты"
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
    owner = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.SET_NULL, related_name='Сообщения',
                              verbose_name='Владелец')

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "сообщения"
        ordering = ["updated_at", "topic"]

    def __str__(self):
        return self.topic


class Mailing(models.Model):
    """
    модель рассылки сообщения списку получателей
    """
    send_start = models.DateTimeField(verbose_name="Дата и время первой отправки")
    send_stop = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    status = models.CharField(max_length=9, verbose_name="Статус", default='Создана')

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="mailings",
        verbose_name="Сообщение",
    )

    clients = models.ManyToManyField(Client, verbose_name="Получатели")
    owner = models.ForeignKey(CustomUser, editable=False, on_delete=models.SET_NULL, related_name='Рассылки',
                              verbose_name='Владелец', blank=True, null=True)

    enabled = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "рассылки"
        ordering = ["-id"]
        permissions = [('can_disable_mailing', 'Can enable and disable mailing'), ]

    def send(self):
        attempt = Attempt()
        attempt.mailing = self
        attempt.owner = self.owner
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

    owner = models.ForeignKey(CustomUser, editable=False, on_delete=models.SET_NULL, related_name='Попытки_рассылок+',
                              verbose_name='Владелец', blank=True, null=True)

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="Рассылка",
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "попытки рассылки"
        ordering = ["-id"]
