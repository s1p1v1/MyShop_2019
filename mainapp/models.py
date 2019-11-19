from django.db import models

from authapp.models import ShopUser


# Create your models here.
class Country(models.Model):
    name = models.CharField(verbose_name='страна изготовления', max_length=64, unique=True)
    is_active = models.BooleanField(verbose_name='действительная', default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='страна изготовления')
    caption = models.CharField(verbose_name='название продукта', max_length=128, unique=True)
    quality = models.TextField(verbose_name='признаки продукта', blank=True)
    preference = models.TextField(verbose_name='применение продукта', blank=True)
    image_src = models.ImageField(upload_to='products_images', blank=True)
    producer = models.CharField(verbose_name='организация - изготовитель продукта', max_length=60, blank=True)
    brand = models.CharField(verbose_name='фирменный знак продукта', max_length=60, blank=True)
    alco = models.CharField(verbose_name='крепкость продукта', max_length=60, blank=True)
    vol = models.CharField(verbose_name='объем продукта', max_length=5, blank=True)
    class_c = models.CharField(verbose_name='класс продукта', max_length=10, blank=True)
    age = models.IntegerField(verbose_name='возраст продукта', null=True)
    cost = models.DecimalField(verbose_name='цена продукта', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='количество на складе', default=0)
    comment = models.TextField(verbose_name='описание продукта', blank=True)
    is_active = models.BooleanField(verbose_name='действительный', default=True)

    def __str__(self):
        return "{} ({})".format(self.caption, self.country.name)


class Rating(models.Model):
    RATING = ((0, 'отсутствует'), (1, 'неуд'), (2, 'удовл'), (3, 'хор'), (4, 'отл'))
    rating = models.IntegerField(choices=RATING, default=0, db_index=True,
                                 verbose_name='рейтинг продукта от пользователя')
    rating_product = models.OneToOneField(Product, on_delete=models.PROTECT, unique=False)
    rating_user = models.ManyToManyField(ShopUser, unique=False)

    def __str__(self):
        return str(self.rating)
