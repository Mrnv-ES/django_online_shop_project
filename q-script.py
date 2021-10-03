import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mygeekshop.settings')

import django

django.setup()

from django.db import connection
from django.db.models import Q
from mainapp.models import Product
from mainapp.views import db_profile_by_type


def my_func_1():
    test_products = Product.objects.filter(
        Q(category__name='дом') |
        Q(category__name='дача')
    ).select_related('category')

    print(len(test_products))

    db_profile_by_type('q-script', '', connection.queries)


def my_func_2():
    from datetime import timedelta
    from django.db.models import F, When, Case, IntegerField, DecimalField
    from ordersapp.models import OrderItem

    ACTION_1 = 1
    ACTION_2 = 2
    ACTION_EXPIRED = 3

    action_1__time_delta = timedelta(hours=12)
    action_2__time_delta = timedelta(days=1)

    action_1_discount = 0.3
    action_2_discount = 0.15
    action_exp_discount = 0.05

    action_1__condition = Q(order__update_date__lte=F('order__add_date') + action_1__time_delta)
    action_2__condition = Q(order__update_date__gt=F('order__add_date') + action_1__time_delta) & \
                     Q(order__update_date__lte=F('order__add_date') + action_2__time_delta)
    action_exp__condition = Q(order__update_date__gt=F('order__add_date') + action_2__time_delta)

    action_1__order = When(action_1__condition, then=ACTION_1)
    action_2__order = When(action_2__condition, then=ACTION_2)
    action_expired__order = When(action_exp__condition, then=ACTION_EXPIRED)

    action_1__price = When(action_1__condition, then=F('product__price') * F('qty') * action_1_discount)
    action_2__price = When(action_2__condition, then=F('product__price') * F('qty') * -action_2_discount)
    action_expired__price = When(action_exp__condition, then=F('product__price') * F('qty') * action_exp_discount)

    orderitems_test = OrderItem.objects.annotate(
        action_order=Case(
            action_1__order,
            action_2__order,
            action_expired__order,
            output_field=IntegerField(),
        )).annotate(
        discounted_price=Case(
            action_1__price,
            action_2__price,
            action_expired__price,
            output_field=DecimalField(),
        )).order_by('action_order', 'discounted_price'). \
        select_related('order', 'product')

    for orderitem in orderitems_test:
        print(f'{orderitem.action_order:2}: заказ №{orderitem.pk:3}:\
                   {orderitem.product.name:20}: скидка\
                   {abs(orderitem.discounted_price):6.2f} руб. | \
                   {orderitem.order.update_date - orderitem.order.add_date}')


if __name__ == '__main__':
    my_func_2()
