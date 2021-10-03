from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import random
#from django.views.decorators.cache import cache_page
from mainapp.models import Product, ProductCategory
from mygeekshop import settings


def get_products():
    if settings.LOW_CACHE:
        key = 'all_products'
        products = cache.get(key)
        if products is None:
            products = Product.get_items()
            cache.set(key, products)
        return products
    return Product.get_items()


def get_products_by_category(pk):
    if settings.LOW_CACHE:
        key = f'products_of_{pk}_category_'
        products = cache.get(key)
        if products is None:
            products = Product.get_items().filter(category_id=pk)
            cache.set(key, products)
        return products
    return Product.get_items().filter(category_id=pk)


def get_hot_product():
    products_id = get_products().values_list('id', flat=True)
    rand_id = random.choice(products_id)
    return Product.objects.get(pk=rand_id)


def similar_products(hot_product):
    return Product.get_items().filter(category=hot_product.category). \
               exclude(pk=hot_product.pk)[:3]


def index(request):
    context = {
        'page_name': 'танцевальный магазин',
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    hot_product = get_hot_product()

    context = {
        'page_name': 'каталог',
        'hot_product': hot_product,
        'similar_products': similar_products(hot_product),
    }
    return render(request, 'mainapp/products.html', context)


def product_page(request, pk):
    product = get_object_or_404(Product, pk=pk)

    context = {
        'page_name': 'страница продукта',
        'product': product,
    }
    return render(request, 'mainapp/product_page.html', context)


# @cache_page(3600)   # кэширование контроллера, корзина на главной не обновляется!
def category(request, pk):
    page_num = request.GET.get('page', 1)
    if pk == 0:
        category = {'pk': 0, 'name': 'все'}
        products = get_products()
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = get_products_by_category(pk)

    products_paginator = Paginator(products, 4)
    try:
        products = products_paginator.page(page_num)
    except PageNotAnInteger:
        products = products_paginator.page(1)
    except EmptyPage:
        products = products_paginator.page(products_paginator.num_pages)

    context = {
        'page_name': 'товары категории',
        'category': category,
        'products': products,
    }
    return render(request, 'mainapp/category_products.html', context)


def contact(request):
    contacts = [
        {'city': 'Москва',
         'phone': '8-925-765-82-09',
         'email': 'msk@mygeekshop.ru',
         'location': 'ул. Ленина, 8',},
        {'city': 'Екатеринбург',
         'phone': '8-925-357-22-54',
         'email': 'ekb@mygeekshop.ru',
         'location': 'ул. Морозова, 43',},
        {'city': 'Владивосток',
         'phone': '8-925-354-98-12',
         'email': 'vld@mygeekshop.ru',
         'location': 'ул. Парковая, 15',}
    ]

    context = {
        'page_name': 'контакты',
        'contacts': contacts,
    }
    return render(request, 'mainapp/contact.html', context)


def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(pk=pk).first()
        return JsonResponse({'price': product.price if product else 0})


def db_profile_by_type(sender, query_type, queries):
    print(f'db profile {query_type} for {sender}:')
    for query in filter(lambda x: query_type in x, map(lambda x: x['sql'], queries)):
        print(query)


@receiver(pre_save, sender=ProductCategory)
def update_product_category(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)
