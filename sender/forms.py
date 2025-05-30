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
        # exclude = ['status']
        fields = ['send_start', 'send_stop', 'message']
        widgets = {
            'send_start': DateTimePickerInput(),
            'send_stop': DateTimePickerInput(),
            # 'clients': CheckboxSelectMultiple(attrs={'rows': 50})
        }

    # def __init__(self, *args, **kwargs):
    #     super(MailingCreateForm, self).__init__(*args, **kwargs)

        # for check in self.fields['clients'].widget.subwidgets:
        #     check.data.attrs.update({'class': 'custom-checkbox-class',})
        # self.fields['clients'].widget.attrs.update({
        #     'class': 'custom-checkbox-class',
        # })