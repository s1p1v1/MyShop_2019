import datetime
import json
import os
import random

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from authapp.models import ShopUser
from basket.models import Basket
from mainapp.forms import ProdRatingForm, SearchForm, ProdSortForm
from mainapp.models import Country, Product, Rating

JSON_PATH = 'mainapp/json'


def loadFromJSON(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


# Create your views here.
def main(request):
    basket = getBasket(request.user)
    # content = {'links_menu': links_menu, 'basket': basket}
    content = {'basket': basket}

    return render(request, 'mainapp/index.html', content)


def getBasket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def getHotProduct():
    products = Product.objects.exclude(is_active=False).order_by('id')
    return random.sample(list(products), 1)[0]


def getSameProducts(hot_product, sort_variant=0, reverse=0):
    print('getSameProducts:', sort_variant, reverse)
    # same_products = Product.objects.exclude(pk=hot_product.pk).filter(is_active=True).order_by('id')
    # Вариант сортировки
    if sort_variant == 0:  # по умолчанию
        sv = 'id'
    elif sort_variant == 1:  # по цене
        sv = 'cost'
    else:  # по рейтингу
        # sv = 'rating'
        sv = 'age'
    # Направление сортировки
    if not reverse:  # 0 - по убыванию (по умолчанию)
        same_products = Product.objects.exclude(pk=hot_product.pk).filter(is_active=True).order_by(sv).reverse()
    else:  # 1 - по возрастанию
        same_products = Product.objects.exclude(pk=hot_product.pk).filter(is_active=True).order_by(sv)
    return same_products


def getSearchProduct(search):
    search_products = Product.objects.exclude(is_active=False).order_by('id').filter(caption__icontains=search)
    return search_products


def search(request):
    basket = getBasket(request.user)

    # Результат поиска
    form = SearchForm()
    search_query = request.GET.get('search', '')
    if search_query != '':
        # Товар найден...
        search_product = getSearchProduct(search_query)
        print('начало постраничного цикла ', search_query, search_product)

        # экземпляр класса Paginator (2 - объектов на странице)
        paginator = Paginator(search_product, 2)
        print('paginator in')
        print(request.GET.dict())
        page = request.GET.get('page', 1)
        print('номер текущей страницы с сайта =', page)

        try:
            # получение объектов нужной сраницы
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            # последняя страница
            products_paginator = paginator.page(paginator.num_pages)
        print('всего страниц пагинатора =', paginator.num_pages)
        print('номер текущей страницы пагинатора =', products_paginator.number)
        print('всего объектов в пагинаторе =', paginator.count)
        print('объекты в пагинаторе ->', products_paginator.object_list)
        print('paginator out')
        search_product = products_paginator

        content = {
            'search_query': search_query,
            'same_products': search_product,
            'page': page,
            'basket': basket,
            'form': form,
        }

    else:
        # Товар не найден...
        content = {
            'same_products': 0,
            'basket': basket,
            'form': form,
        }

    return render(request, 'mainapp/search.html', content)


# def catalogue(request, pk=0, page=1):
def catalogue(request):
    print('request - параметры запроса')
    print(request.GET.dict())
    try:
        # получение объектов запроса
        print('получение страны из запроса')
        pk = request.GET.get('country')
        pk = int(pk)
    except:
        print('сбой получения страны из запроса')
        pk = 0
    print('страна из запроса -> ', pk)

    try:
        # получение объектов запроса
        print('получение страницы из запроса')
        page = request.GET.get('page')
        page = int(page)
    except:
        print('сбой получения страницы из запроса')
        page = 1
    print('страница из запроса -> ', pk)

    # Добавляем форму выбора страны и сортировки товаров в шаблон
    form = ProdSortForm()

    # Читаем данные из формы ?
    if form.is_valid():
        pk = int(form.cleaned_data['country'])  # страна
        sv = int(form.cleaned_data['price_rating'])  # вариант сортировки (1 - по цене/2 - рейтингу)
        r = int(form.cleaned_data['sorting_direction'])  # 0 - убывание/1 - возрастание
        print('страна {}, поле сортировки {},  убыв/возр {} из формы -> '.format(pk, sv, r))

    # Читаем данные из запроса
    try:
        # получение объектов запроса
        print('получение вида сортировки из запроса')
        sv = request.GET.get('price_rating')
        sv = int(sv)
    except:
        print('сбой получения вида сортировки из запроса')
        # параметры сортировки по умолчанию
        sv = 0  # по id продукта
    print('вид сортировки  из запроса -> ', sv)

    try:
        # получение объектов запроса
        print('получение направления сортировки из запроса')
        r = request.GET.get('sorting_direction')
        r = int(r)
    except:
        print('сбой получения направления сортировки из запроса')
        # параметры сортировки по умолчанию
        r = 1  # возрастание
    print('направление сортировки из запроса -> ', r)

    basket = getBasket(request.user)

    # Формируем список товаров с учетом сортировки
    # countrys = Country.objects.filter(is_active=True)
    hot_product = getHotProduct()

    same_products = getSameProducts(hot_product, sv, r)

    print('список всех товаров, кроме горячего ->', same_products)

    if pk:
        country = get_object_or_404(Country, pk=pk)
        same_products = same_products.filter(country=pk).order_by('id')
        print('список товаров страны {} -> {}'.format(country, same_products))

    else:
        country = {
            'pk': 0,
            'name': 'Все'
        }
        print('список товаров страны {} -> {}'.format(country['name'], same_products))

    # экземпляр класса Paginator (2 - объектов на странице)
    paginator = Paginator(same_products, 2)
    print('paginator in')
    try:
        # получение объектов нужной сраницы
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        # последняя страница
        products_paginator = paginator.page(paginator.num_pages)
    print('всего страниц пагинатора =', paginator.num_pages)
    print('номер текущей страницы =', products_paginator.number)
    print('всего объектов в пагинаторе =', paginator.count)
    print('объекты в пагинаторе ->', products_paginator.object_list)
    print(page)
    print('paginator out')

    # same_products = products_paginator

    content = {
        'page': page,
        'hot_product': hot_product,
        # 'same_products': same_products,
        'same_products': products_paginator,
        'basket': basket,
        'country': country,
        # 'countrys': countrys,
        'form': form,
        'price_rating': sv,
        'sorting_direction': r
    }
    return render(request, 'mainapp/catalogue.html', content)


def contact(request):
    visit_date = datetime.datetime.now()
    # content = {'links_menu': links_menu, 'visit_date': visit_date}
    content = {'visit_date': visit_date}

    return render(request, 'mainapp/contact.html', content)


def country(request, pk=None):
    basket = getBasket(request.user)
    countrys = Country.objects.all()
    # country = get_object_or_404(Country, pk=int(pk))
    products = Product.objects.filter(country__pk=pk).order_by('caption')
    content = {
        'countrys': countrys,
        'products': products,
        'basket': basket
    }
    return render(request, 'mainapp/country.html', content)


def good(request, pk=None):
    print('good', pk)
    basket = getBasket(request.user)
    countrys = Country.objects.all()
    same_product = Product.objects.get(pk=pk)

    print(request.META.get('HTTP_REFERER'))

    # Рейтинг продукта

    # Считаем усредненный рейтинг продукта по частным оценкам пользователей
    rfp = Rating.objects.filter(rating_product_id=pk)
    lrfp = len(rfp)  # число частных оценок продукта
    print('lrfp =', lrfp)
    r_product = 0

    if lrfp:
        r_product = rfp.aggregate(models.Avg('rating'))['rating__avg']
        print('r_product', r_product)
        if r_product == 4:
            rating_product = 'отлично'
        elif r_product >= 3:
            rating_product = 'хорошо'
        elif r_product >= 2:
            rating_product = 'удовлетворительно'
        else:
            rating_product = 'неудовлетворительно'

    else:
        rating_product = 'не оценен'

    user = request.user
    u_is_auth = user.is_authenticated
    print(u_is_auth)

    get_form = False
    form = None

    if u_is_auth:
        is_app = is_appreciated(id_product=pk, id_user=user.id)
        print('is_app', is_app)
        # if not lrfp or not is_app:
        if not is_app:
            # Предоставить форму для оценки продукта (на шаблоне)
            get_form = True
            form = ProdRatingForm(data=request.POST)
            # Запись рейтинга продукта pk от пользователя id_user в БД
            print('запись рейтинга для продукта {}... '.format(pk))
            print(request.method)
            print(form.is_valid())
            # if request.method == 'POST':
            # form = ProdRatingForm(request.POST)
            if request.method == 'POST' and form.is_valid():
                # if form.is_valid():
                # Получение из формы рейтинга продукта
                rating = form.cleaned_data['rating']
                print('рейтинг из формы =', rating)
                # Зпись рейтинга продукта в БД
                rp = Rating.objects.create(rating=rating, rating_product=Product.objects.get(id=pk))

                # Добавление в БД связи рейтинга с оценивающим пользователем
                rp.rating_user.add(ShopUser.objects.get(id=user.id))

                print('get_form =', get_form)
                return redirect(reverse('good', args=(pk,)))

    print('get_form =', get_form)
    content = {'countrys': countrys, 'same_product': same_product, 'rating_product': rating_product,
               'r_product': r_product, 'basket': basket, 'get_form': get_form, 'form': form}

    return render(request, 'mainapp/good.html', content)


def is_appreciated(id_product, id_user):
    print('product ', id_product, 'user ', id_user)
    # Был ли оценен продукт id_product пользователем id_user?
    try:
        # prod_rat = Rating.objects.get(rating_product_id=id_product)
        prod_rat = Rating.objects.filter(rating_product_id=id_product).all()
        print('product ', id_product)

        for pr in prod_rat:
            print('user ', id_user, ' оценил продукт ', pr.rating_product.id,
                  pr.rating_user.all().filter(id=id_user).exists())
            if pr.rating_user.all().filter(id=id_user).exists():
                print('Пользователь ранее оценил продукт')
                return 1  # оценен
    except:
        # pass
        print('Пользователь ранее не оценивал продукт')
        return 0  # не оценен


"""
@login_required
def product_rating_accounting (request, form, id_product):
    # Запись рейтинга продукта id_product от пользователя id_user в БД
    print('запись рейтинга... для продукта {}'.format(id_product))
    if form.is_valid():
        id_user = request.user.id
        # Получение из формы рейтинга продукта
        rating = form.cleaned_data['rating']
        print('рейтинг из формы =', rating)
        # Зпись рейтинга продукта в БД
        rp = Rating.objects.create(rating=rating, rating_product=Product.objects.get(id=id_product))

        # Добавление в БД связи рейтинга с оценивающим пользователем
        rp.rating_user.add(ShopUser.objects.get(id=id_user))

    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # return HttpResponseRedirect(reverse('good'))
    # return HttpResponseRedirect(reverse('good', kwargs={'id_product': id_product}))
    print('...выполнена')
    html = '''
    <a href="{% url 'mainapp:good' id_product %}"> Оценить </a>
    '''
    return HttpResponse(html)
"""


def product_rating_accounting_ajax(request, id_product):
    if request.is_ajax():
        id_user = request.user.id
        # Получение из формы рейтинга продукта
        rating = ProdRatingForm.rating

        # Зпись рейтинга продукта в БД
        rp = Rating.objects.create(rating=rating, rating_product=Product.objects.get(id=id_product))

        # Добавление в БД связи рейтинга с оценивающим пользователем
        rp.rating_user.add(ShopUser.objects.get(id=id_user))

        result = render_to_string('mainapp/includes/inc_good_rating.html')
        return JsonResponse({'result': result})
