from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import login
from django.urls import reverse_lazy,reverse

from .forms import CustomUserCreationForm
from .models import CustomUser
from django.views.generic import TemplateView,DetailView,ListView,CreateView
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from .models import *

class HomeView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = DishGeneralCategories.objects.all()[:5]
        return context


class UserProfileView(DetailView):
    model = CustomUser
    slug_field = 'slug'
    template_name = 'userProfile.html'

class CategoryListView(ListView):
    model = DishGeneralCategories
    context_object_name = 'categories'
    template_name = 'categories.html'

class CategoryDetailView(DetailView):
    model = DishGeneralCategories
    template_name = 'category_detail.html'
    context_object_name = 'category'


class RegisterUser(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register_user.html'
    extra_context = {'title': "Регистрация"}
    # success_url = reverse_lazy('user_profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
    def get_success_url(self):
        # Перенаправляем на профиль с slug нового пользователя
        return reverse('user_profile', kwargs={'slug': self.object.slug})

def get_cities(request):
    term = request.GET.get('term', '').lower()
    cities = City.objects.filter(name__istartswith=term)[:10]  # Ограничим до 10 результатов
    results = [{'label': f"{city.name} ({city.region})", 'value': city.pk} for city in cities]
    print(f"Term: {term}, Found cities: {list(cities)}")
    print("Returning JSON:", results)
    return JsonResponse(results, safe=False)


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)