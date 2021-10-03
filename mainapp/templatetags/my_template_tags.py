from django import template
from django.conf import settings

register = template.Library()


def default_products_image(string):
    if not string:
        string = 'products_images/default.jpg'

    return f'{settings.MEDIA_URL}{string}'


register.filter('default_products_image', default_products_image)


@register.filter(name='default_user_avatar')
def default_user_avatar(string):
    if not string:
        string = 'avatars/default.jpg'
    return f'{settings.MEDIA_URL}{string}'
