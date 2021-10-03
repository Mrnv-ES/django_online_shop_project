from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from adminapp.forms import AdminShopUserUpdateForm, AdminProductCategoryCreationForm, AdminProductUpdateForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from mainapp.views import db_profile_by_type


class SuperUserCheckMixin:
    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PageTitleMixin:
    page_title = None
    page_title_key = 'page_title'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.page_title_key] = self.page_title
        return context


@user_passes_test(lambda user: user.is_superuser)
def index(request):
    users = get_user_model().objects.all()
    context = {
        'page_title': 'админка/пользователи',
        'users': users,
    }
    return render(request, 'adminapp/index.html', context)


# class ShopUserListView(SuperUserCheckMixin, PageTitleMixin, ListView):
#     model = ShopUser
#     page_title = 'админка/пользователи'
#     paginate_by = 2
#     queryset = ShopUser.objects.all()


@user_passes_test(lambda user: user.is_superuser)
def delete_user(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if not user.is_active or request.method == 'POST':
        if user.is_active:
            user.is_active = False
            user.save()
        return HttpResponseRedirect(reverse('my_admin:index'))
    context = {
        'page_title': 'админка/пользователи/удаление',
        'delete_user': user,
    }
    return render(request, 'adminapp/delete_user.html', context)


# @user_passes_test(lambda user: user.is_superuser)
# def update_user(request, user_pk):
#     user = get_object_or_404(get_user_model(), pk=user_pk)
#     if request.method == 'POST':
#         user_form = AdminShopUserUpdateForm(request.POST, request.FILES, instance=user)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('my_admin:index'))
#     else:
#         user_form = AdminShopUserUpdateForm(instance=user)
#
#     context = {
#         'page_title': 'админка/пользователи/редактирование',
#         'user_form': user_form,
#     }
#     return render(request, 'adminapp/shopuser_form.html', context)


class ShopUserUpdateByAdmin(SuperUserCheckMixin, PageTitleMixin, UpdateView):
    model = get_user_model()
    form_class = AdminShopUserUpdateForm
    success_url = reverse_lazy('my_admin:index')
    pk_url_kwarg = 'user_pk'
    page_title = 'админка/пользователи/редактирование'


# @user_passes_test(lambda user: user.is_superuser)
# def categories(request):
#     context = {
#         'page_title': 'админка/категории',
#         'category_list': ProductCategory.objects.all(),
#     }
#     return render(request, 'adminapp/productcategory_list.html', context)


class ProductCategoryListView(SuperUserCheckMixin, PageTitleMixin, ListView):
    model = ProductCategory
    page_title = 'админка/категории'
    paginate_by = 2
    queryset = ProductCategory.objects.all()


class ProductCategoryCreateView(SuperUserCheckMixin, PageTitleMixin, CreateView):
    # fields = '__all__' # задаем либо fields, либо form_class
    form_class = AdminProductCategoryCreationForm
    model = ProductCategory
    success_url = reverse_lazy('my_admin:categories')
    # template_name = 'adminapp/productcategory_form.html' # вместо этого создаем mainapp в templates и помещаем туда productcategory_form.html
    page_title = 'админка/категории/создание'


class ProductCategoryUpdateView(SuperUserCheckMixin, PageTitleMixin, UpdateView):
    form_class = AdminProductCategoryCreationForm
    model = ProductCategory
    success_url = reverse_lazy('my_admin:categories')
    page_title = 'админка/категории/редактирование'


class ProductCategoryDeleteView(SuperUserCheckMixin, PageTitleMixin, DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('my_admin:categories')
    page_title = 'админка/категории/удаление'


@user_passes_test(lambda u: u.is_superuser)
def category_products(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    object_list = category.product_set.all()
    context = {
        'page_title': f'категория {category.name}/продукты',
        'category': category,
        'object_list': object_list
    }
    return render(request, 'mainapp/category_products_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def create_category_product(request, category_pk):
    category = get_object_or_404(ProductCategory, pk=category_pk)
    if request.method == 'POST':
        form = AdminProductUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('my_admin:category_products', kwargs={'pk': category.pk}))
    else:
        form = AdminProductUpdateForm(initial={'category': category,})

    context = {
        'page_title': 'продукты/создание',
        'form': form,
        'category': category,
    }
    return render(request, 'mainapp/product_update.html', context)


class ProductDetailView (SuperUserCheckMixin, PageTitleMixin, DetailView):
    model = Product
    page_title = 'админка/продукты'
