import json
import os

from django.core.management.base import BaseCommand

from authapp.models import ShopUser

# from django.contrib.auth.models import User


JSON_PATH = 'mainapp/fixtures'


def loadFromJSON(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


class Command(BaseCommand):
    # help = 'Fill DB new data'
    help = 'Add DB new data'

    def handle(self, *args, **options):
        '''
        countrys = loadFromJSON('country')

        #Country.objects.all().delete()
        for country in countrys:
            new_country = Country(**country)
            new_country.save()
        
        products = loadFromJSON('products')
        
        #Product.objects.all().delete()
        for product in products:
            category = product["country"]
            print(category)
            # Получаем категорию по имени
            _category = Country.objects.get(id=category)
            # Заменяем название категории объектом
            product['country'] = _category
            new_product = Product(**product)
            new_product.save()

        User.objects.all().delete()
        # Создаем суперпользователя при помощи менеджера модели
        #super_user = User.objects.create_superuser('django', 'django@geekshop.local', 'geekbrains')
        '''
        super_user = ShopUser.objects.create_superuser('django', 'q@q.local', 'geekbrains', age='32')
