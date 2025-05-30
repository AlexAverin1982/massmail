from django import forms
from .models import Client
from .mixins import FormControlMixin

class ClientCreateForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'email', 'comment']