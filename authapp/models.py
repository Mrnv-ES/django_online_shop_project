import hashlib
import random
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.timezone import now
from mygeekshop.settings import DOMAIN_NAME, EMAIL_HOST_USER, ACTIVATION_KEY_TTL


class ShopUser(AbstractUser):
    age = models.PositiveIntegerField('возраст', null=True)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    activation_key = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # def basket_total_cost(self):
    #     return sum(el.product_cost for el in self.basket.all())
    #
    # def basket_quantity(self):
    #     return sum(el.quantity for el in self.basket.all())

########################################################
    @cached_property
    def basket_items(self):
        return self.basket.select_related('product').all()

    def basket_total_cost(self):
        return sum(el.product_cost for el in self.basket_items)

    def basket_quantity(self):
        return sum(el.quantity for el in self.basket_items)

########################################################

    def send_confirmation_email(self):
        activate_link = reverse('auth:activate', kwargs={'email': self.email, 'activation_key': self.activation_key})
        sbj = f'Подтверждение аккаунта {self.username}'
        msg = f'Чтобы подтвердить аккаунт {self.username} на портале {DOMAIN_NAME} перейдите по ссылке: \n{DOMAIN_NAME}{activate_link} '
        return send_mail(sbj, msg, EMAIL_HOST_USER, [self.email], fail_silently=False)

    @property
    def is_activation_key_expired(self):
        return now() - self.date_joined > timedelta(hours=ACTIVATION_KEY_TTL)

    def set_activation_key(self):
        salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:6]
        self.activation_key = hashlib.sha1((self.email + salt).encode('utf-8')).hexdigest()


class ShopUserProfile(models.Model):
    MALE = 'm'
    FEMALE = 'w'

    GENDER_CHOICES = ((MALE, 'Мужской'), (FEMALE, 'Женский'))

    user = models.OneToOneField(ShopUser, primary_key=True, on_delete=models.CASCADE)
    tags = models.CharField(verbose_name='Теги', max_length=128, blank=True)
    about_me = models.TextField(verbose_name='О себе', blank=True)
    gender = models.CharField(verbose_name='Пол', max_length=1, choices=GENDER_CHOICES, blank=True)
