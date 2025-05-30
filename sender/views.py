from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from typing_extensions import Any


from .models import Client
from .forms import ClientCreateForm

class HomeView(generic.ListView):
    model = Client
    template_name = "home.html"
    context_object_name = 'clients'
    paginate_by = 10

    def get_queryset(self):
        
        key_name = f"clients_queryset"
        queryset = cache.get(key_name)
        if not queryset:
            queryset = Client.objects.all()
            cache.set(key_name, queryset, 60 * 15)

        return queryset


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



