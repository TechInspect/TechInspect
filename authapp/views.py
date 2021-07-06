from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from authapp.models import User


# Create your views here.
# login with CBV
class UserLoginView(LoginView):
    context = 'Вход'
    template_name = 'authapp/login.html'
    model = User
    form_class = UserLoginForm
    fields = ['username', 'password']


class RegisterCreateView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    success_message = 'Вы успешно зарегистрировались'
    # reverse_lazy - для получения урла - для класса
    success_url = reverse_lazy('auth:login')


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
