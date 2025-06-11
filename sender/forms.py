import datetime

from django import forms
# from django.forms import CheckboxSelectMultiple
# from django.http import HttpResponseRedirect

from .models import Client, Message, Mailing
from .mixins import FormControlMixin
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class ClientCreateForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'email', 'comment', ]


class MessageCreateForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ['topic', 'text', ]


class MailingCreateForm(FormControlMixin, forms.ModelForm):
    clients = forms.ModelMultipleChoiceField(queryset=Client.objects.all())

    class Meta:
        model = Mailing
        fields = '__all__'  # no use, form is customized, but without it server won't start
        # exclude = ['status']
        STATUS_CHOICES = (('Создана', 'Создана'), ('Запущена', 'Запущена'), ('Завершена', 'Завершена'),)
        widgets = {
            'send_start': DateTimePickerInput(),
            'send_stop': DateTimePickerInput(),
            'status': forms.Select(attrs={'id': 'status_select'}, choices=STATUS_CHOICES),
            'owner': forms.Select(attrs={'id': 'owner_select'}),
            'enabled': forms.CheckboxInput(attrs={'class': 'custom-checkbox-class'})
            # 'clients': CheckboxSelectMultiple(queryset=Client.objects.all().filter(owner=self.request.user))
        }

    def clean(self):
        cleaned_data = super().clean()
        send_start = cleaned_data.get('send_start')
        send_stop = cleaned_data.get('send_stop')
        now = datetime.datetime.now()
        if not send_stop:
            self._errors["send_stop"] = self.error_class(['Время завершения рассылки не указано'])
            raise forms.ValidationError('Время завершения рассылки не указано')
            # self.add_error('send_stop', 'Время завершения рассылки не указано')
        elif now.timestamp() > send_stop.timestamp():
            # print('----------------error!!')
            self._errors["send_stop"] = self.error_class(['Время завершения рассылки указано как уже прошедшее'])
            raise forms.ValidationError('Время завершения рассылки указано как уже прошедшее')
            # self.add_error('send_stop', 'Время завершения рассылки указано как уже прошедшее')
            # del cleaned_data['send_stop']

        elif send_start.timestamp() >= send_stop.timestamp():
            # print('----------------error!!')
            self._errors["send_stop"] = self.error_class(['Промежуток времени работы рассылки указан неверно'])
            raise forms.ValidationError('Промежуток времени работы рассылки указан неверно')
            # del cleaned_data['send_stop']
            # self.add_error('send_stop', 'Промежуток времени работы рассылки указан неверно')
        # status = cleaned_data.get('status')
        # print(f'self.data: {self.data}')
        # print(f'status: {status}')
        # print(f'cleaned_data: {cleaned_data}')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance is not None:
            if hasattr(instance, 'owner'):
                self.user = instance.owner
            # print(f"self.user: {self.user}")
        else:
            self.user = kwargs.pop('user', None)
        super(MailingCreateForm, self).__init__(*args, **kwargs)

        self.fields['enabled'].widget.attrs.update({
            'class': 'custom-checkbox-class'
        })

        if self.user:
            self.fields['clients'].queryset = Client.objects.all().filter(owner=self.user)
            self.fields['message'].queryset = Message.objects.all().filter(owner=self.user)

    # for check in self.fields['clients'].widget.subwidgets:
    #     check.data.attrs.update({'class': 'custom-checkbox-class',})
    # self.fields['clients'].widget.attrs.update({
    #     'class': 'custom-checkbox-class',
    # })
