from django import forms
from .models import Client, Message
from .mixins import FormControlMixin

class ClientCreateForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'email', 'comment']

class MessageCreateForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ['topic', 'text']

