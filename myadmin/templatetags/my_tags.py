import math

from django import template

register = template.Library()

URL_PREFIX = '/media/'


def clown_style(name):
    result = []
    for i in range(len(name)):
        if i % 2 == 0:
            new_letter = name[i].upper()
        else:
            new_letter = name[i].lower()
        result.append(new_letter)
    result = ''.join(result)
    return result


# Так оформлено название "горячего" товара
@register.filter(name='expanded_text')
def expanded_text(string):
    return '-'.join(list(string))


@register.filter(name='ruble_penny')
def ruble_penny(x):
    y = math.modf(x)
    r = int(y[1])
    p = int(y[0] * 100)
    return '{} руб. {} коп.'.format(r, p)


def media_folder_products(string):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам продуктов
    products_images/product1.jpg --> /media/products_images/product1.jpg
    """
    if not string:
        string = 'products_images/default.jpg'

    new_string = "{}{}".format(URL_PREFIX, string)

    return new_string


@register.filter(name='media_folder_users')
def media_folder_users(string):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам пользователей
    users_avatars/user1.jpg --> /media/users_avatars/user1.jpg
    """
    if not string:
        string = 'users_avatars/default.jpg'

    new_string = "{}{}".format(URL_PREFIX, string)

    return new_string


register.filter('media_folder_products', media_folder_products)
register.filter('clown_style', clown_style)


# register.filter('media_folder_users', media_folder_users)

@register.filter(name='short_name')
def short_name(string):
    return string[:3]


if __name__ == '__main__':
    '''
    print(media_folder_products('products_images/product1.jpg'))
    print(media_folder_products(''))

    print(clown_style('Пользователь1'))
    '''

    print(expanded_text('Пользователь1'))
    print(ruble_penny(876.2345))
