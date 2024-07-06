from django.urls import path
from . import views
from users.views import MakeForm, SeeForm, Profile

urlpatterns = [

    path('', views.MainPage.as_view(), name='home'),
    path('menu/', views.menu_view, name='menu'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('create_form_person/', MakeForm.as_view(), name='create_form_person'),
    path('form_person/<slug:form_person_slug>', SeeForm.as_view(), name='form_person'),

    path('exercises/', views.Exercises.as_view(), name='exercises'),
    path('exercise/<slug:exercise_slug>/', views.ShowExercisesPage.as_view(), name='exercise'),

    path('profile/', Profile.as_view(), name='profile'),
    path('blogs/', views.blogs, name='blogs'),
    path('blog/<slug:blog_slug>/', views.show_blog, name='blog'),
    path('blog_category/<slug:blog_category_slug>/', views.show_blog_category, name='blog_category'),

]
