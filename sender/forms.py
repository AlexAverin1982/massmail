import datetime

from django import forms
from django.forms import CheckboxSelectMultiple

from .models import Client, Message, Mailing
from .mixins import FormControlMixin
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

class ClientCreateForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'email', 'comment']

class MessageCreateForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ['topic', 'text']


class MailingCreateForm(FormControlMixin, forms.ModelForm):
    # my_field = forms.ModelMultipleChoiceField(queryset=Client.objects.all(), required=False,
    #                                           widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = Mailing
        exclude = ['status']
        widgets = {
            'send_start': DateTimePickerInput(),
            'send_stop': DateTimePickerInput(),
            # 'clients': CheckboxSelectMultiple(attrs={'class': 'form-check', })
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
            print('----------------error!!')
            self._errors["send_stop"] = self.error_class(['Время завершения рассылки указано как уже прошедшее'])
            raise forms.ValidationError('Время завершения рассылки указано как уже прошедшее')
            # self.add_error('send_stop', 'Время завершения рассылки указано как уже прошедшее')
            # del cleaned_data['send_stop']

        elif send_start.timestamp() >= send_stop.timestamp():
            print('----------------error!!')
            self._errors["send_stop"] = self.error_class(['Промежуток времени работы рассылки указан неверно'])
            raise forms.ValidationError('Промежуток времени работы рассылки указан неверно')
            # del cleaned_data['send_stop']
            # self.add_error('send_stop', 'Промежуток времени работы рассылки указан неверно')
        # status = cleaned_data.get('status')
        # print(f'self.data: {self.data}')
        # print(f'status: {status}')
        # print(f'cleaned_data: {cleaned_data}')
        return cleaned_data

    # def __init__(self, *args, **kwargs):
    #     super(MailingCreateForm, self).__init__(*args, **kwargs)

        # for check in self.fields['clients'].widget.subwidgets:
        #     check.data.attrs.update({'class': 'custom-checkbox-class',})
        # self.fields['clients'].widget.attrs.update({
        #     'class': 'custom-checkbox-class',
        # })