from django.conf import settings
from django.test import TestCase, Client
from authapp.models import ShopUser


class UserManagementTest(TestCase):
    fixtures = ['mainapp.json']

    def setUp(self):
        self.client = Client()
        self.superuser = ShopUser.objects.create_superuser(
            'test_user_1', 'test_user_1@geekshop.local', 'geekbrains'
        )
        self.user = ShopUser.objects.create_user(
            'test_user_2', 'test_user_2@geekshop.local', 'geekbrains'
        )
        self.user_with__first_name = ShopUser.objects.create_user(
            'test_user_3', 'test_user_3@geekshop.local', 'geekbrains', first_name='Test'
        )

    def user_login_test(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['page_title'], 'главная')
        self.assertNotContains(response, 'Пользователь', status_code=200)

        self.client.post('/auth/login/',
                         data={'username': 'test_user_4',
                               'password': 'geekbrains'})

        response = self.client.get('/')
        self.assertEqual(self.user, response.context['user'])
        self.assertContains(response, 'Пользователь', status_code=200)

    def basket_login_redirect_test(self):
        response = self.client.get('/basket/')
        self.assertEqual('/auth/login/?next=/basket/', response.url)
        self.assertEqual(302, response.status_code)

        self.client.login(username='test_user_4', password='geekbrains')

        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual([], list(response.context['user'].basket_items))
        self.assertEqual('/basket/', response.request['PATH_INFO'])
        self.assertIn('Ваша корзина,', response.content.decode('utf-8'))

    def user_logout_test(self):
        self.client.login(username='tarantino', password='geekbrains')

        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)

        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

    def user_register_test(self):
        response = self.client.get('/auth/user/register/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('регистрация', response.context['page_title'])
        self.assertTrue(response.context['user'].is_anonymous)

        new_user_data = {
            'username': 'test_user_5',
            'first_name': 'Louis',
            'last_name': 'Tomlinson',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'test_user_5@geekshop.local',
            'age': '40'
        }

        response = self.client.post('/auth/user/register/', data=new_user_data)
        self.assertEqual(response.status_code, 302)

        new_user = ShopUser.objects.get(username=new_user_data['username'])
        self.assertFalse(new_user.is_active)

        activation_url = f"{settings.DOMAIN_NAME}/auth/user/verify/{new_user_data['email']}/" \
                         f"{new_user.activation_key}/"

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)

        self.client.login(
            username=new_user_data['username'],
            password=new_user_data['password1']
        )

        response = self.client.get('/')
        self.assertContains(response, text=new_user_data['first_name'], status_code=200)

    def user_wrong_register_test(self):
        new_user_data = {
            'username': 'test_user_6',
            'first_name': 'Andrew',
            'last_name': 'Styles',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'test_user_6@geekshop.local',
            'age': '13'
        }

        response = self.client.post('/auth/user/register/', data=new_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'age', 'Вам еще рано пользоваться этим сайтом!')
