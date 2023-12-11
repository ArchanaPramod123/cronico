from django.urls import path
from .import views

urlpatterns = [
    path('',views.admin_login,name='adminlogin'),
    path('admin_index/',views.admin_index,name='admin_index'),
    path('admin_category/',views.admin_category,name='admin_category'),
    path('admin_category_insert/',views.admin_category_insert,name='admin_category_insert'),
    path('admin_category_edit/<int:id>',views.admin_category_edit,name='admin_category_edit'), 
    path('admin_product/',views.admin_product,name='admin_product'),   
    path('admin_product_add/',views.admin_product_add,name='admin_product_add'),  
    path('admin_product_edit/<int:id>',views.admin_product_edit,name='admin_product_edit'),
    path('customers/',views.customers,name='customers'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
]
