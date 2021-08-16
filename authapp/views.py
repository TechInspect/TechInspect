from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.core.mail import send_mail

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from authapp.models import User


# Create your views here.
# login with CBV
class UserLoginView(LoginView):
    # extra_context = {
    #     'title': 'Вход',
    # }
    template_name = 'authapp/login.html'
    model = User
    form_class = UserLoginForm
    fields = ['username', 'password']

    @method_decorator(user_passes_test(lambda u: u.is_anonymous, login_url='car_park:index', redirect_field_name=''))
    def dispatch(self, request, *args, **kwargs):
        return super(UserLoginView, self).dispatch(request, *args, **kwargs)


class RegisterCreateView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    success_message = 'Вы успешно зарегистрировались'
    # reverse_lazy - для получения урла - для класса
    success_url = reverse_lazy('auth:login')

    def get_context_data(self, **kwargs):
        context = super(RegisterCreateView, self).get_context_data()
        context['title'] = 'Techinspect - Регистрация'
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            messages.success(self.request, 'Вы успешно зарегистрировались!')
            user = form.save()
            if send_verify_mail(user):
                print('success sending')
            else:
                print('sending failed')
            return HttpResponseRedirect(reverse('auth:login'))
        else:
            messages.error(self.request, 'Такой пользователь или почта уже существуют!')
            return HttpResponseRedirect(reverse('auth:register'))


def verify(request, email, activation_key):
    user = User.objects.filter(email=email).first()
    print(user)
    if user:
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Учетная запись активирована")
        return HttpResponseRedirect(reverse('main:index'))
    return HttpResponseRedirect(reverse('index'))


def send_verify_mail(user):
    subject = 'Verify your account'
    link = reverse('auth:verify', args=[user.email, user.activation_key])
    message = f'{settings.DOMAIN_NAME}{link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


class UserLogoutView(LogoutView):
    next_page = 'main:index'


class ProfileUpdateView(UpdateView):
    model = User
    template_name = 'authapp/profile.html'
    form_class = UserProfileForm

    def get_success_url(self):
        return reverse_lazy('auth:profile', kwargs={'pk': self.object.id})  # object because model = User

    def get_context_data(self, **kwargs):
        # получаем контекст у родителя
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileUpdateView, self).dispatch(request, *args, **kwargs)
