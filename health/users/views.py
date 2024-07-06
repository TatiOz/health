from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from health import settings
from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm, FormPersonForm
from users.models import FormPersonComplains


# Create your views here.

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    extra_context = {'title': 'Авторизация'}


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {
        'title': "Профиль пользователя",
        'default_image': settings.DEFAULT_USER_IMAGE,
    }

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"


class MakeForm(LoginRequiredMixin, CreateView):
    model = FormPersonComplains
    template_name = 'users/create_form_person.html'
    fields = ['complaints', 'medical_history', 'photo', 'is_published']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Форма для описания жалоб'

        return context

    def form_valid(self, form):
        form_instance = form.save(commit=False)
        form_instance.profile_id = self.request.user
        form_instance.save()
        return super().form_valid(form)


class SeeForm(DetailView):
    template_name = 'users/form_person.html'
    slug_url_kwarg = 'form_person_slug'

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(FormPersonComplains, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_instance = self.get_object()
        context['chronic_diseases'] = form_instance.chronic_diseases
        context['height'] = form_instance.height
        context['weight'] = form_instance.weight
        context['date_birth'] = form_instance.date_birth

        return context


class Profile(LoginRequiredMixin, ListView):
    paginate_by = 7
    template_name = 'users/show_publications.html'

    def get_queryset(self):
        return FormPersonComplains.objects.filter(profile_id_id=self.request.user.id)
