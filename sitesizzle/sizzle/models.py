from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser,UserManager

class DishGeneralCategories(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.CharField(max_length=255, default='sizzle/images/mini-profile-foto-default.svg')
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Категория блюд"
        verbose_name_plural = "Категории блюд"
        ordering = ['order']

    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null = True)
    price = models.FloatField()
    category = models.ForeignKey(DishGeneralCategories,on_delete=models.PROTECT,related_name='dishes')


class City(models.Model):
    region = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ['name', 'region']

    def __str__(self):
        return f"{self.name} ({self.region})"
    

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_surname = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(unique=True)
    number_phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, 
                            choices=[('client', 'Client'), ('chef', 'Chef'), ('admin', 'Admin'), ('support', 'Support')], 
                            default='client')
    accepted_phone = models.BooleanField(default=False)
    accepted_email = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_slug(self):
        return self.slug

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
        # except:
            
class ChefProfiles(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'chef'},primary_key=True)
    bio = models.TextField(blank=True, null=True)
    rating = models.FloatField(default=0.0)
    photo = models.ImageField(upload_to='chef_photos/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    accepted_passport = models.BooleanField(default=False)
    payment_details = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Профиль повара: {self.user.first_name} {self.user.last_name}"

class UserClient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'client'},primary_key=True)
    rating = models.FloatField(default=0.0)
    photo = models.ImageField(upload_to='client_photos/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Профиль клиента: {self.user.first_name} {self.user.last_name}"

__all__ = ['City', 'Dish', 'DishGeneralCategories','CustomUser','ChefProfiles','UserClient']