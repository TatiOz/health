from datetime import datetime
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from users.models import FormPersonComplains
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля",
                                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    this_year = datetime.now().year
    date_birth = forms.DateField(label='Дата рождения',
                                 widget=forms.SelectDateWidget(years=tuple(range(this_year - 100, this_year - 18))))

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'first_name', 'last_name', 'date_birth', 'height', 'weight',
                  'chronic_diseases']
        # fields = '__all__'
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'height': forms.TextInput(
                attrs={'placeholder': 'Введите рост (см)', 'class': 'form-control', 'type': 'number'}),
            'weight': forms.TextInput(
                attrs={'placeholder': 'Введите вес (кг)', 'class': 'form-control', 'type': 'number'}),
            'chronic_diseases': forms.Textarea(
                attrs={'placeholder': 'Напишите ваши хронические болезни', 'class': 'form-control', 'rows': 8}),
        }


class FormPersonForm(forms.ModelForm):
    class Meta:
        model = FormPersonComplains
        fields = ['complaints', 'medical_history', 'photo', 'is_published']
        # fields= '__all__'
        widgets = {
            'birth_year': forms.DateInput(attrs={'type': 'date'}),
            'height': forms.TextInput(
                attrs={'placeholder': 'Введите рост (см)', 'class': 'form-control', 'type': 'number'}),
            'weight': forms.TextInput(
                attrs={'placeholder': 'Введите вес (кг)', 'class': 'form-control', 'type': 'number'}),
            'medical_history': forms.Textarea(
                attrs={'placeholder': 'Когда начались жалобы и как развивались сипмтомы', 'class': 'form-control',
                       'rows': 8}),

        }
        labels = {'slug': 'URL'}
