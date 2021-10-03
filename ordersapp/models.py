from django.db import models
from django.contrib.auth import get_user_model
from django.utils.functional import cached_property

from mainapp.models import Product


class Order(models.Model):
    STATUS_FORMING = 'f'
    STATUS_PROCEEDING = 'pr'
    STATUS_PAID = 'p'
    STATUS_READY = 'r'
    STATUS_CANCELED = 'c'

    STATUS_CHOICES = (
        (STATUS_FORMING, 'формируется'),
        (STATUS_PROCEEDING, 'обрабатывается'),
        (STATUS_PAID, 'оплачен'),
        (STATUS_READY, 'готов'),
        (STATUS_CANCELED, 'отменен'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    add_date = models.DateTimeField('время', auto_now_add=True, db_index=True)
    update_date = models.DateTimeField('время', auto_now=True)
    status = models.CharField('статус', db_index=True, max_length=1, choices=STATUS_CHOICES, default=STATUS_FORMING)
    is_active = models.BooleanField(verbose_name='активен', db_index=True, default=True)

    @cached_property
    def is_forming(self):
        return self.status == self.STATUS_FORMING

    @cached_property
    def total_quantity(self):
        return sum(map(lambda x: x.quantity, self.order_items.all()))

    @cached_property
    def total_cost(self):
        return sum(map(lambda x: x.product_cost, self.order_items.all()))

    @property
    def my_summary(self):
        order_items = self.order_items.all()
        return {
            'total_quantity': sum(map(lambda x: x.quantity, order_items)),
            'total_cost': sum(map(lambda x: x.product_cost, order_items))
        }

    def delete(self, using=None, keep_parents=False):
        for item in self.order_items.all():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()

    class Meta:
        ordering = ('-add_date',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class OrderItemManager(models.QuerySet):
    def delete(self):
        print('OrderItemManager delete')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('количество', default=0)
    add_date = models.DateTimeField('время', auto_now_add=True)
    update_date = models.DateTimeField('время', auto_now=True)


    @cached_property
    def product_cost(self):
        return self.product.price * self.quantity

    @classmethod
    def get_item(cls, pk):
        return cls.objects.select_related('product').filter(pk=pk).first()

