from django.urls import path
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('user/register/', authapp.register, name='register'),
    path('user/edit/', authapp.edit, name='edit'),
    path('user/activate/<str:email>/<str:activation_key>/', authapp.activate, name='activate'),
    # path('user/after_register/', authapp.after_register, name='after_register'),
]
