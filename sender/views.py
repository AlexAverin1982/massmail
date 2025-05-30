from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from typing_extensions import Any

from .models import Client, Message
from .forms import ClientCreateForm, MessageCreateForm


class HomeView(generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'clients': Client.objects.all().order_by('full_name'),
            'messages': Message.objects.all().order_by('-updated_at'),
        })
        return context


class ClientCreateView(generic.CreateView):
    model = Client
    form_class = ClientCreateForm
    # fields = ['name', 'price', 'category', 'image', 'description']
    template_name = 'new_client.html'
    context_object_name = 'client'

    extra_context = {
        'title': 'Добавление клиента',
    }
    success_url = reverse_lazy('home')

    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)


# @method_decorator(cache_page(60 * 15), name='dispatch')
class ClientDetailView(generic.DetailView):
    model = Client
    template_name = "client_details.html"
    context_object_name = 'client'


# LoginRequiredMixin,
class ClientUpdateView(generic.UpdateView):
    model = Client
    form_class = ClientCreateForm
    template_name = 'new_client.html'
    # success_url = reverse_lazy('home')
    extra_context = {
        'title': 'Редактирование данных клиента',
        'client_editing_mode': True,
    }

    def get_success_url(self):
        return reverse("client_details", kwargs=self.kwargs)


class ClientDeleteView(generic.DeleteView):
    model = Client
    success_url = reverse_lazy("home")
    context_object_name = 'client'
    template_name = 'delete_client.html'

    def post(self, request, *args, **kwargs) -> Any:
        obj = Client.objects.get(id=kwargs['pk'])
        super(ClientDeleteView, self).post(request, *args, **kwargs)
        return redirect('home')


#######################################################################################################################


class MessageCreateView(generic.CreateView):
    model = Message
    form_class = MessageCreateForm
    template_name = 'new_message.html'
    context_object_name = 'message'

    extra_context = {
        'title': 'Новое сообщение',
    }
    success_url = reverse_lazy('home')


class MessageDetailView(generic.DetailView):
    model = Message
    template_name = "message_details.html"
    context_object_name = 'message'


class MessageUpdateView(generic.UpdateView):
    model = Message
    form_class = MessageCreateForm
    template_name = 'new_message.html'
    # success_url = reverse_lazy('home')
    extra_context = {
        'title': 'Редактирование сообщения',
        'message_editing_mode': True,
    }

    def get_success_url(self):
        return reverse("message_details", kwargs=self.kwargs)


class MessageDeleteView(generic.DeleteView):
    model = Message
    success_url = reverse_lazy("home")
    context_object_name = 'message'
    template_name = 'delete_message.html'

    def post(self, request, *args, **kwargs) -> Any:
        obj = Message.objects.get(id=kwargs['pk'])
        super(MessageDeleteView, self).post(request, *args, **kwargs)
        return redirect('home')

#######################################################################################################################
