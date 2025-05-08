from .models import City

def city(request):
    return {'City': City}