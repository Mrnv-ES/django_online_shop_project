import adminapp.views as adminapp
from django.urls import path

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.index, name='index'),
    path('user/delete/<int:user_pk>/', adminapp.delete_user, name='delete_user'),
    # path('user/update/<int:user_pk>/', adminapp.update_user, name='update_user'),
    # path('user/update/<int:pk>/', adminapp.ShopUserUpdateByAdmin.as_view(), name='update_user'),
    path('user/update/<int:user_pk>/', adminapp.ShopUserUpdateByAdmin.as_view(), name='update_user'),
    # path('categories/', adminapp.categories, name='categories'),
    path('categories/', adminapp.ProductCategoryListView.as_view(), name='categories'),
    path('category/create/', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', adminapp.ProductCategoryDeleteView.as_view(), name='category_delete'),
    path('category/<int:pk>/products/', adminapp.category_products, name='category_products'),
    path('category/<int:category_pk>/product/create/', adminapp.create_category_product, name='create_category_product'),
    path('product/<int:pk>/', adminapp.ProductDetailView.as_view(), name='product_detail_view'),
]
