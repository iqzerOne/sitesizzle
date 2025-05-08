from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import CustomUser,City
from django.core.validators import RegexValidator
import re


class CustomUserCreationForm(UserCreationForm):
    phone_validator = RegexValidator(regex=r'^\+\d{1}\(\d{3}\)\s\d{3}-\d{2}-\d{2}$', message='Только цифры!')

    role = forms.ChoiceField(
        choices=[('client', 'Клиент'), ('chef', 'Шеф')],
        label="Регистрация как"
    )

    city_id_hide = forms.CharField(widget=forms.HiddenInput(), required=False)

    city = forms.CharField(
        label = "Город",
        widget = forms.TextInput(attrs={'data-cities-url': '/get-cities/'}),
    )

    number_phone = forms.CharField(
        label='Номер мобильного телефона',
        validators=[phone_validator],
        widget=forms.TextInput(
            attrs = {
                'placeholder' : '+7(999) 111-22-33',
                'type': 'tel',
                'pattern': r'^\+\d{1}\(\d{3}\)\s\d{3}-\d{2}-\d{2}$',
                'title': 'Разрешены только цифры'
            }
        )
    )

    first_name = forms.CharField(
        label='Ваше имя'
    )
    last_name = forms.CharField(
        label='Ваша фамилия'
    )
    user_surname = forms.CharField(
        label='Ваше отчество(необязательно)'
    )

    class Meta:
        model = CustomUser
        model.role
        fields = ('first_name','last_name','username','user_surname','number_phone','email','role','city')

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email
    
    def clean_number_phone(self):
        number_phone = self.cleaned_data['number_phone']

        cleaned_phone = re.sub(r'[\s\-\(\)]+','',number_phone)

        print(cleaned_phone)

        if not re.match(r'^(\+7)\d{10}$',cleaned_phone):
            raise forms.ValidationError("Номер не соответствует формату")

        if CustomUser.objects.filter(number_phone=cleaned_phone).exists():
            raise forms.ValidationError("Такой телефон уже существует!")
        
        return cleaned_phone


    def clean(self):
        cleaned = super().clean()
        city_id = cleaned.get('city_id_hide')
        city_name = cleaned.get('city')
        print(city_id,city_name)

        if city_id:
            try:
                city_obj = City.objects.get(pk=int(city_id))
            except (City.DoesNotExist,ValueError):
                self.add_error('city_id_hide','Неверный город выберите из списка.')
            else:
                cleaned['city'] = city_obj
                return cleaned
        
        if not city_name:
            self.add_error('city', 'Нужно указать город.')
            return cleaned
        qs = City.objects.filter(name__istartswith=city_name)
        count = qs.count()
        if count == 0:
            self.add_error('city', 'Город не найден. Выберите из списка или уточните ввод.')
        elif count > 1:
            names = ', '.join(c.name for c in qs)
            self.add_error('city', 
                f'Найдено несколько городов: {names}. Выберите из списка.')
        else:
            cleaned['city'] = qs.first()

        return cleaned
    

    def save(self, commit=True):
        user = super().save(commit=False)
        # Устанавливаем город из очищенных данных
        user.city = self.cleaned_data['city']
        if commit:
            user.save()
            print(self.cleaned_data['role'])
            print("Создан новый пользователь с id:", user.id)
            if self.cleaned_data['role'] == 'client':
                print("Проверка",self.cleaned_data['role'])
                from .models import UserClient
                UserClient.objects.get_or_create(user=user)
            elif self.cleaned_data['role'] == 'chef':
                print("Проверка",self.cleaned_data['role'])
                from .models import ChefProfiles
                ChefProfiles.objects.get_or_create(user=user)
        return user