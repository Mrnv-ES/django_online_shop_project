# import pickle
# from django.core.management.base import BaseCommand
# from authapp.models import ShopUser
# from mainapp.models import Product, ProductCategory
#
#
# def write_to_pickle(data, file_name):
#     with open(file_name, 'wb') as infile:
#         return pickle.dump(data, infile)
#
#
# class Command(BaseCommand):
#     help = 'Dump data from db'
#
#     def handle(self, *args, **options):
#         product_schema = ('id', 'name', 'description', 'short_description')
#         items = []
#         for item in ProductCategory.objects.all():
#             # print(vars(item))
#             items.append({key: val
#                           for key, val in vars(item).items()
#                           if key in product_schema})
#         print(items)

        # items = load_from_json('mainapp/json/products.json')
        # for item in items:
        #     category = ProductCategory.objects.get(name=item['category'])
        #     item['category'] = category
        #     Product.objects.create(**item)
        #
        # if not ShopUser.objects.filter(username='django').exists():
        #     ShopUser.objects.create_superuser('django', 'djando@example.ru', 'geekbrains')
