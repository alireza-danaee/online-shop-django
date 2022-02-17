from django.urls import path
from . import views
app_name = 'shop'








urlpatterns = [
    path('' , views.product_list , name='product_list'),
    path('page/<int:page>' , views.product_list , name='product_list'),
    path('category/<slug:slug>' , views.category_list , name='category_list'),
    
    
]