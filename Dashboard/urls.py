from django.urls import path
from .views import *

urlpatterns=[
    path('', home, name='home'),
    path('Users/user_view', all_user, name='all_user'),
    path('Users/Add', add_user, name='add_user'),
    path('Items/All', all_products_view, name='all_products_view'),
    path('Items/Add', create_item, name='create_item'),
    path('Invoice/All', all_invoice_list, name='all_invoice_list'),

]