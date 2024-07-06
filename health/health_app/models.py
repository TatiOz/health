from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField


# Create your models here.
class Health(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    content = models.TextField(blank=True)
    link = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('exercise', kwargs={'exercise_slug': self.slug})


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=1)


class Blog(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    subtitle = models.CharField(max_length=255, blank=True, verbose_name='Подзаголовок')
    slug = AutoSlugField(populate_from="title", slugify_function=slugify, verbose_name='Путь',
                         unique=True)  # unique=True,
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', default=None,
                              blank=True, null=True, verbose_name='Фото')
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.IntegerField(choices=Status.choices, default=Status.DRAFT, verbose_name='Статус')
    category = models.ForeignKey('Blog_category', on_delete=models.SET_NULL, verbose_name='Категория', null=True)
    object = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time_create']
        indexes = [models.Index(fields=['-time_create'])]

    def get_absolute_url(self):
        return reverse('blog', kwargs={'blog_slug': self.slug})


class Blog_category(models.Model):
    name = models.CharField(max_length=100, db_index=True, blank=True, null=True)
    slug = models.SlugField(max_length=255, db_index=True, blank=True, null=True)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog_category', kwargs={'blog_category_slug': self.slug})


class UploadFiles(models.Model):
    file = models.FileField(upload_to='upload_model', blank=True, null=True)


class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    url_name = models.CharField(max_length=200)
    authenticated_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title


