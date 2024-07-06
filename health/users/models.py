from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField


# Create your models here.
class User(AbstractUser):
    photo = models.ImageField(upload_to='users/%Y/%m/%d', default=None, blank=True, null=True,
                              verbose_name='Фото профиля')
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")
    chronic_diseases = models.TextField(max_length=1000, blank=True, verbose_name='Хронические болезни')

    height = models.CharField(max_length=255, verbose_name='Рост', blank=True, null=True, )
    weight = models.CharField(max_length=255, verbose_name='Вес', blank=True, null=True, )


class FormPersonComplains(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовать"

    complaints = models.TextField(max_length=1000, blank=True, verbose_name='Жалобы')
    medical_history = models.TextField(blank=True, null=True, verbose_name='Анамнез')
    slug = AutoSlugField(populate_from="complaints", slugify_function=slugify, verbose_name='Путь',
                         unique=True)  # unique=True,
    photo = models.ImageField(upload_to='users/%Y/%m/%d', default=None, blank=True, null=True,
                              verbose_name='Добавить фото')
    time_create = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    time_update = models.DateTimeField(blank=True, null=True, auto_now=True)
    is_published = models.IntegerField(blank=True, null=True, choices=Status.choices, default=Status.DRAFT, verbose_name='Статус')
    profile_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='form_person_complaints',
                                   verbose_name='Пользователь')
    objects = models.Manager()


    def __str__(self):
        return self.slug

    class Meta:
        ordering = ['-time_create']
        indexes = [models.Index(fields=['-time_create'])]

    def get_absolute_url(self):
        return reverse('form_person', kwargs={'form_person_slug': self.slug})

    @property
    def chronic_diseases(self):
        return self.profile_id.chronic_diseases if self.profile_id else None

    @property
    def height(self):
        return self.profile_id.height if self.profile_id else None

    @property
    def weight(self):
        return self.profile_id.weight if self.profile_id else None

    @property
    def date_birth(self):
        return self.profile_id.date_birth if self.profile_id else None



