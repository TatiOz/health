from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render,  get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from .models import Health, Blog, Blog_category, MenuItem

def menu_view(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'base.html', {'menu': menu_items})

class MainPage(TemplateView):
    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ['health_app/authenticated_home.html']
        else:
            return ['health_app/index.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

def about(request):
    return render(request, 'health_app/about.html',
                  {'title': 'O сайте'})

class Exercises(LoginRequiredMixin, ListView):
    template_name = 'health_app/exercises.html'
    context_object_name = 'exercises'  # имя которое отображается в шаблоне для отображения статей
    extra_context = {
        'title': 'Упраженения',
        'menu': MenuItem.objects.all(),
    }

    def get_queryset(self):
        return Health.objects.filter(is_published=True)

class ShowExercisesPage(LoginRequiredMixin, DetailView):
    model = Health
    template_name = 'health_app/exercise_page.html'
    slug_url_kwarg = 'exercise_slug'
    context_object_name = 'exercise'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = MenuItem.objects.all()
        context['title'] = context['exercise'].title
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Health.objects.filter(is_published=True), slug=self.kwargs[self.slug_url_kwarg])

@login_required
def blogs(request):
    menu = MenuItem.objects.all()
    blog_posts = Blog.published.all()
    data = {'title': 'Блог',
            'menu': menu,
            'blog_posts': blog_posts,
            }
    return render(request, 'health_app/blogs.html', context=data)

@login_required
def show_blog(request, blog_slug):  # page
    menu = MenuItem.objects.all()
    blog = get_object_or_404(Blog.published.all(), slug=blog_slug)
    data = {
        'title': f'Блог: {blog.title}',
        'menu': menu,
        'blog': blog,
        'selected_cat': 1,
    }
    return render(request, 'health_app/blog_page.html', context=data)

@login_required
def show_blog_category(request, blog_category_slug):
    menu = MenuItem.objects.all()
    blog_category = get_object_or_404(Blog_category, slug=blog_category_slug)
    blog = Blog.published.filter(category_id=blog_category).select_related('category')
    # blog_category.blog_set.all()
    data = {
        'title': f'Рубрика: {blog_category.name}',
        'menu': menu,
        'blog': blog,
        'selected_cat': blog_category.pk,
    }
    return render(request, 'health_app/blogs.html', context=data)

def contact(request):
    return render(request, 'health_app/contacts.html')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Ooops!<h1>")
