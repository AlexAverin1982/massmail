# from http.client import HTTPResponse
# from bootstrap_datepicker_plus.widgets import DateTimePickerInput
# from django.db.transaction import commit
# from django.forms import CheckboxSelectMultiple, SelectMultiple
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy, reverse
# from django.core.cache import cache
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator

from typing_extensions import Any

from .models import Client, Message, Mailing, Attempt
from .forms import ClientCreateForm, MessageCreateForm, MailingCreateForm


class HomeView(generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'clients': Client.objects.all(),
            'messages': Message.objects.all().order_by('-updated_at'),
            'mailings': Mailing.objects.all(),
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

class MailingCreateView(generic.edit.CreateView):
    model = Mailing
    form_class = MailingCreateForm
    template_name = 'new_mailing.html'
    context_object_name = 'mailing'

    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'possible_clients': Client.objects.all(),
            'title': 'Новая рассылка',
        })
        return context

    def post(self, request, *args, **kwargs) -> Any:
        # request.POST = request.POST.copy()
        # request.POST['clients'] = Client.objects.all()
        data = MailingCreateForm(request.POST)
        # print(f"clients: {request.POST.get('clients')}")

        if data.is_valid():
            print('here-------------------------------')
            update = data.save(commit=False)
            update.save()
            data.save_m2m()
            return HttpResponseRedirect(reverse('home'))
        else:
            kwargs['errors_data'] = self.get_form().errors
            return HttpResponseRedirect(reverse('errors'))


class MailingDetailView(generic.DetailView):
    model = Mailing
    template_name = "mailing_details.html"
    context_object_name = 'mailing'


class MailingUpdateView(generic.UpdateView):
    model = Mailing
    form_class = MailingCreateForm
    template_name = 'new_mailing.html'

    # extra_context = {
    #     'title': 'Редактирование рассылки',
    #     'mailing_editing_mode': True,
    #     'possible_clients': Client.objects.all(),
    # }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'title': 'Редактирование рассылки',
            'mailing_editing_mode': True,
        })

        # print(f"context: {context}")
        print(f"context.mailing clients: {context['mailing'].clients.all()}")
        return context

    def get_success_url(self):
        return reverse("mailing_details", kwargs=self.kwargs)


class MailingDeleteView(generic.DeleteView):
    model = Mailing
    success_url = reverse_lazy("home")
    context_object_name = 'mailing'
    template_name = 'delete_mailing.html'

    def post(self, request, *args, **kwargs) -> Any:
        obj = Mailing.objects.get(id=kwargs['pk'])
        super(MailingDeleteView, self).post(request, *args, **kwargs)
        return redirect('home')


class MailingErrorsView(generic.TemplateView):
    template_name = 'errors.html'

class ForceSendMailingView(generic.DetailView):
    template_name = 'force_send_mailing.html'

    def get(self, request, *args, **kwargs):
        print('force mailing to be sent manually...')
        mailing = get_object_or_404(Mailing, pk=kwargs.get('pk', -1))
        mailing.send()
        return redirect('home')



class MailingAttemptsListView(generic.TemplateView):
    # model = Attempt
    template_name = "mailing_attempts.html"
    # context_object_name = 'items'
    # paginate_by = 50

    # extra_context = {
    #     'categories': Category.objects.all().order_by('name'),
    # }

    # def get_queryset(self, **kwargs):
        # queryset = super().get_queryset(**kwargs)
        # print(f"queryset : {queryset}")
        # queryset = cache.get('products_queryset')
        # if not queryset:
        #     user = self.request.user
        #     if is_moder(user) or is_superuser(user):
        #         products = self.model.objects.all()
        #     else:
        #         products = self.model.objects.filter(is_published=True)
        #     queryset = products.order_by("-created_at")
        #     cache.set('products_queryset', queryset, 60 * 15)
        # mailing = get_object_or_404(Mailing, pk=kwargs.get('pk', -1))
        # print(mailing)
        # print(f"kwargs.pk: {kwargs.get('pk')}")
        # pk = self.request['pk']
        # if pk:
        #     attempts = self.model.objects.filter(mailing=pk)
        #     queryset = attempts.order_by("-created_at")
        # else:
        #     raise Http404(f"Записи попыток для рассылки {self} не найдены")
        #
        # return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        mailing = get_object_or_404(Mailing, pk=kwargs.get('pk', -1))
        attempts = Attempt.objects.all()      #.filter(mailing=pk).order_by("-date_time")
        print(f"mailing: {mailing}")
        # print(f"attempts: {attempts}")

        # print(f"kwargs: {kwargs}")
        context.update({
            'mailing': mailing,
            'attempts': attempts,
        })
        return context

