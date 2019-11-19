from django.contrib import admin

from basket.models import Basket
from mainapp.models import Country, Product

# Register your models here.
admin.site.register(Country)
admin.site.register(Product)
admin.site.register(Basket)
