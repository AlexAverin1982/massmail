from django.contrib.auth import authenticate
# from django.contrib.messages.context_processors import messages
from django.core.management.base import BaseCommand
# from django.contrib.auth.models import Group, Permission
from django.shortcuts import get_object_or_404

from sender.models import Mailing, Attempt


class Command(BaseCommand):
    help = "Add access control groups to the database"

    def handle(self, *args, **kwargs) -> None:
        # ask login email
        email = input('Введите свой логин (email): ')
        password = input('Введите пароль: ')
        user = authenticate(username=email, password=password)
        if user:
            if user.is_active:
                mailing_id = int(input('Введите id рассылки: '))
                mailing = get_object_or_404(Mailing, pk=mailing_id)
                mailing.send()
                attempts = Attempt.objects.filter(mailing=mailing_id).order_by('-date_time')
                if attempts:
                    message = f"попытка рассылки сообщения '{mailing.message.topic}' {attempts[0].date_time}"
                    if attempts[0].is_successful:
                        message += ' прошла успешно'
                    else:
                        message += 'не удалась'
                    print(message)
