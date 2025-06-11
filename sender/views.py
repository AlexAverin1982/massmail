# from http.client import HTTPResponse
# from bootstrap_datepicker_plus.widgets import DateTimePickerInput
# from django.db.transaction import commit
# from django.forms import CheckboxSelectMultiple, SelectMultiple
# import django.utils.functional
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache

from typing_extensions import Any

from .models import Client, Message, Mailing, Attempt
from .forms import ClientCreateForm, MessageCreateForm, MailingCreateForm


class HomeView(generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not isinstance(self.request.user, AnonymousUser):
            context.update({
                'clients': Client.objects.all().filter(owner=self.request.user),
                'messages_to_send': Message.objects.all().filter(owner=self.request.user),
                'mailings': Mailing.objects.all().filter(owner=self.request.user),
                'total_mailings_count':
                    Mailing.objects.all().filter(owner=self.request.user).count(),
                'active_mailings_count':
                    Mailing.objects.all().filter(owner=self.request.user).filter(status='Запущена').count(),
                'clients_count':
                    Client.objects.all().filter(owner=self.request.user).count()
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

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.model.owner = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs) -> Any:
        request.POST = request.POST.copy()
        request.POST['owner'] = request.user
        data = ClientCreateForm(request.POST)
        print(f"request.user: {request.user}")

        if data.is_valid():
            data.instance.owner = request.user
            update = data.save(commit=False)
            update.owner = request.user
            update.save()
            data.save_m2m()
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            print(f"request.POST: {request.POST}")
            print(f"data: {data}")
            errors = self.get_form().errors
            print(f"errors: {errors}")
            # kwargs['errors_data'] = self.get_form().errors
            return HttpResponseRedirect(reverse('errors'))


@method_decorator(cache_page(60 * 15), name='dispatch')
class ClientDetailView(generic.DetailView):
    model = Client
    template_name = "client_details.html"
    context_object_name = 'client'


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
        Client.objects.get(id=kwargs['pk'])
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

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.model.owner = self.request.user
        self.object.owner = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs) -> Any:
        request.POST = request.POST.copy()
        request.POST['owner'] = request.user
        data = MessageCreateForm(request.POST)  # ФОРМА А НЕ ВИД!!!
        print(f"request.user: {request.user}")
        # эта песня посвещена борьбе за мир!
        if data.is_valid():
            data.instance.owner = request.user
            update = data.save(commit=False)
            update.owner = request.user
            update.save()
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            print(f"request.POST: {request.POST}")
            print(f"data: {data}")
            errors = self.get_form().errors
            print(f"errors: {errors}")
            # kwargs['errors_data'] = self.get_form().errors
            return HttpResponseRedirect(reverse('errors'))


@method_decorator(cache_page(60 * 20), name='dispatch')
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
        Message.objects.get(id=kwargs['pk'])
        super(MessageDeleteView, self).post(request, *args, **kwargs)
        return redirect('home')


#######################################################################################################################

class MailingCreateView(generic.edit.CreateView):
    model = Mailing
    form_class = MailingCreateForm
    template_name = 'new_mailing.html'
    context_object_name = 'mailing'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(MailingCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        print(f"kwargs['user']: {kwargs['user']}")
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.model.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(f"user: {self.request.user}")
        context.update({
            'possible_clients': Client.objects.filter(owner=self.request.user),
            'title': 'Новая рассылка',
        })
        return context

    def post(self, request, *args, **kwargs) -> Any:
        request.POST = request.POST.copy()
        request.POST['owner'] = request.user
        request.POST['enabled'] = True  # почему default=True не работает - ненаю
        form_data = MailingCreateForm(request.POST)

        # print(f"clients: {request.POST.get('clients')}")

        if form_data.is_valid():
            form_data.instance.owner = request.user
            mailing = form_data.save(commit=False)
            mailing.owner = request.user
            mailing.save()
            form_data.save_m2m()
            return redirect(reverse_lazy('mailing_details', kwargs={'pk': mailing.id}))
        else:
            print(f"request.POST: {request.POST}")
            print(f"mailing: {form_data}")
            errors = self.get_form().errors
            print(f"errors: {errors}")
            kwargs['errors_data'] = self.get_form().errors
            return HttpResponseRedirect(reverse('errors'))


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
        # print(f"context.mailing clients: {context['mailing'].clients.all()}")
        return context

    def get_success_url(self):
        return reverse("mailing_details", kwargs=self.kwargs)


# @method_decorator(cache_page(60 * 20), name='dispatch')
class MailingDetailView(generic.DetailView):
    model = Mailing
    template_name = "mailing_details.html"
    context_object_name = 'mailing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'owner': self.model.owner,
            'user': self.request.user,
        })

        return context

    def get(self, request, **kwargs):
        if kwargs.get('disable'):
            mailing = get_object_or_404(Mailing, pk=kwargs.get('pk', -1))
            mailing.enabled = not mailing.enabled
            mailing.save()
            return redirect(request.META['HTTP_REFERER'])
        return super().get(self, request, **kwargs)


class MailingDeleteView(generic.DeleteView):
    model = Mailing
    success_url = reverse_lazy("home")
    context_object_name = 'mailing'
    template_name = 'delete_mailing.html'

    def post(self, request, *args, **kwargs) -> Any:
        Mailing.objects.get(id=kwargs['pk'])
        super(MailingDeleteView, self).post(request, *args, **kwargs)
        return redirect('home')


class MailingErrorsView(generic.TemplateView):
    template_name = 'errors.html'


class ForceSendMailingView(generic.DetailView):
    template_name = 'force_send_mailing.html'

    def get(self, request, *args, **kwargs):
        print('force mailing to be sent manually...')
        try:
            mailing = get_object_or_404(Mailing, pk=kwargs.get('pk', -1))
            mailing.send()
        except KeyError as e:
            return reverse_lazy('errors', kwargs={'error_message': e.__str__()})

        return redirect(request.META['HTTP_REFERER'])


# @method_decorator(cache_page(60 * 20), name='dispatch')
class MailingAttemptsListView(generic.TemplateView):
    # model = Attempt
    # template_name = "mailing_attempts.html"
    template_name = "attempts_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        mailing = get_object_or_404(Mailing, pk=kwargs.get('pk', -1))
        attempts = Attempt.objects.filter(mailing=pk)  # .filter(mailing=pk).order_by("-date_time")
        print(f"mailing: {mailing}")
        # print(f"attempts: {attempts}")

        # print(f"kwargs: {kwargs}")
        context.update({
            'mailing': mailing,
            'attempts': attempts,
        })
        return context


class CopyMailingView(generic.DetailView):
    # template_name = 'force_send_mailing.html'

    def get(self, request, *args, **kwargs):
        print('making copy of an existing one...')
        mailing = get_object_or_404(Mailing, pk=kwargs.get('pk', -1))
        mailing.id = None
        mailing.save()
        return redirect(reverse_lazy('mailing_details', kwargs={'pk': mailing.id}))


class MailingListView(generic.ListView):
    model = Mailing
    template_name = "mailing_list.html"
    context_object_name = 'mailings'
    paginate_by = 50

    def get_queryset(self):
        if self.kwargs.get('show_all', False):
            queryset = cache.get('all_mailing_list_queryset')
            if not queryset:
                queryset = Mailing.objects.all().order_by('id')
                cache.set('all_mailing_list_queryset', queryset, 60 * 2)
        else:
            queryset = cache.get('mailing_list_queryset')
            if not queryset:
                queryset = Mailing.objects.all().filter(owner=self.request.user).order_by('id')
                cache.set('mailing_list_queryset', queryset, 60 * 2)
        return queryset


class MessageListView(generic.ListView):
    model = Message
    template_name = "messages_list.html"
    context_object_name = 'messages'
    paginate_by = 50

    def get_queryset(self):
        queryset = cache.get('messages_list_queryset')
        if not queryset:
            queryset = Message.objects.all().filter(owner=self.request.user).order_by('id')
            cache.set('messages_list_queryset', queryset, 60 * 2)
        return queryset


class ClientListView(generic.ListView):
    model = Client
    template_name = "clients_list.html"
    context_object_name = 'clients'
    paginate_by = 50

    def get_queryset(self):
        if self.kwargs.get('show_all', False):
            return Client.objects.all().order_by('id')
        else:
            return Client.objects.filter(owner=self.request.user).order_by('id')


class AttemptListView(generic.ListView):
    model = Attempt
    template_name = "attempts_list.html"
    context_object_name = 'attempts'
    paginate_by = 50

    def get_queryset(self):
        for att in Attempt.objects.all():
            if att.owner is None:
                att.owner = att.mailing.owner
                att.save()

        queryset = cache.get('mailing_attempts_list_queryset')
        if not queryset:
            queryset = Attempt.objects.filter(owner=self.request.user)
            cache.set('mailing_attempts_list_queryset', queryset, 60 * 2)
        return queryset


class StatisticsView(generic.TemplateView):
    template_name = 'statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not isinstance(self.request.user, AnonymousUser):

            mailings_list = []
            mailings = Mailing.objects.filter(owner=self.request.user)
            for m in mailings:
                m_dict = {'id': m.id, 'topic': m.message.topic, 'message_id': m.message.id,
                          'total_attempts': Attempt.objects.filter(mailing=m.id).count(),
                          'successful_attempts': Attempt.objects.filter(mailing=m.id).filter(
                              is_successful=True).count(), }
                if m_dict.get('total_attempts'):
                    mailings_list.append(m_dict)

            context.update({
                'total_attempts_count':
                    Attempt.objects.all().filter(owner=self.request.user).count(),
                'successful_attempts_count':
                    Attempt.objects.all().filter(owner=self.request.user).filter(is_successful=True).count(),
                'mailings_list': mailings_list,
                # 'clients_count':
                #     Client.objects.all().filter(owner=self.request.user).count()
            })
        return context
