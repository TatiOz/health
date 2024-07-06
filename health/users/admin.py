from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from users.models import User
from users.models import FormPersonComplains

admin.site.register(User, UserAdmin)
admin.site.register(FormPersonComplains)

