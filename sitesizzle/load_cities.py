import json
import django
import os

from django.db import IntegrityError

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sitesizzle.settings')
django.setup()

from sizzle.models import City

# Читаем JSON
with open('cities.json', 'r', encoding='utf-8') as f:
    column_data = json.load(f)

# Записываем в модель

if type(column_data) is dict:
    if len(column_data) > 0:
        print("Уникальных пар name+region:", City.objects.values('name', 'region').distinct().count())
        countBefore = City.objects.values('name', 'region').distinct().count()
        try:
            for region, cities in column_data.items():
                for city in cities:
                    obj,created = City.objects.get_or_create(name=city, region=region)
                    try:
                        if created:
                            print("Добавлен:",obj)
                        else:
                            print("В Бд есть такое значение:",obj.name,obj.region)
                    except IntegrityError:
                        print("Ошибка уникальности для города:", city, region)
                    except Exception:
                        print("Другая ошибка при добавлении города:", city, region)
            print(f"Уникальных пар name+region:{City.objects.values('name', 'region').distinct().count()}.До добавления:{countBefore}")
        except IntegrityError:
            print("Ошибка уникальности для города:", city, region)
        except Exception:
            print("Другая ошибка при добавлении города:", city, region)
        except:
            print("Ошибка в добавлении:",region,city)
        # print(City.objects.count())
    else:
        print("JSON пустой")
else:
    print("JSON должен быть словарем")
