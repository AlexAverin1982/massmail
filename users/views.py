from django.urls import reverse_lazy
from django.urls import reverse
from django.views.generic.edit import FormView
from django.views.generic import DetailView, DeleteView, UpdateView, TemplateView, View
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm, CustomUserUpdateForm, LoginForm
from .models import CustomUser
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
# from django.contrib.sites.models import Site
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

User = get_user_model()

class UserLoginView(LoginView):
    form_class = LoginForm
    template_name='login.html'
    next_page='home'

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    success_message = 'Вы успешно зарегистрировались. Можете войти на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # # Функционал для отправки письма и генерации токена
        # token = default_token_generator.make_token(user)
        # uid = urlsafe_base64_encode(force_bytes(user.pk))
        # activation_url = reverse_lazy('confirm_email', kwargs={'uidb64': uid, 'token': token})
        # current_site = Site.objects.get_current().domain
        # current_site = '127.0.0.1'
        # send_mail(
        #     'Подтвердите свой электронный адрес',
        #     f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://{current_site}{activation_url}',
        #     'service.notehunter@gmail.com',
        #     [user.email],
        #     fail_silently=False,
        # )
        return redirect('email_confirmation_sent')

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в наш сервис'
        message = 'Спасибо, что зарегистрировались в нашем сервисе!'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])


class UserProfileView(DetailView):
    model = CustomUser
    template_name = "user_profile.html"
    context_object_name = 'user'
    success_url = reverse_lazy('home')


class UserDeleteView(DeleteView):
    model = CustomUser
    success_url = reverse_lazy("home")
    template_name = 'delete_user.html'


class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'register.html'

    extra_context = {
        'User_editing_mode': True,
    }

    # def __init__(self):
    #     super().__init__()

    def get_success_url(self):
        return reverse("user_profile", kwargs=self.kwargs)


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('email_confirmed')
        else:
            return redirect('email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context
=======
from django.shortcuts import render
