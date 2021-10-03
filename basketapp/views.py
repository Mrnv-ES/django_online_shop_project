from django.db import connection
from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from basketapp.models import BasketElement
from django.contrib.auth.decorators import login_required
from mygeekshop.settings import LOGIN_URL


@login_required
def index(request):
    pass
    # basket = request.user.basketelement_set.all() # из user получаем все его BasketElement
    # basket = BasketElement.objects.filter(user=request.user) # из BasketElement фильтруем по user

    basket = request.user.basket.all()  # для этого не забыть добавить related name для user в basketapp.models
    context = {
        'page_title': 'корзина',
        'basket': basket,
    }
    return render(request, 'basketapp/index.html', context)


@login_required
def add(request, product_pk):
    if LOGIN_URL in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('main:product_page', kwargs={'pk': product_pk}))

    basket_element, _ = BasketElement.objects.get_or_create(
        user=request.user,
        product_id=product_pk
    )
    # basket_element.quantity += 1 # на уровне python-объекта
    basket_element.quantity = F('quantity') + 1  # на уровне бд
    basket_element.save()
    print(connection.queries)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, basket_element_pk):
    element = get_object_or_404(BasketElement, pk=basket_element_pk)
    element.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update(request, basket_element_pk, quantity):
    if request.is_ajax():
        element = BasketElement.objects.filter(pk=basket_element_pk).first()
        if not element:
            return JsonResponse({'status': False})
        if quantity == 0:
            element.delete()
        else:
            element.quantity = quantity
            element.save()
        basket_summary_html = render_to_string('basketapp/includes/basket_summary.html', request=request)
        print(basket_summary_html)
        return JsonResponse({'status': True,
                             'basket_summary': basket_summary_html,
                             'quantity': quantity})
