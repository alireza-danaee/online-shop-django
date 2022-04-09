from django.urls import path
from . import views
app_name = 'shop'








urlpatterns = [
    path('' , views.ProductList.as_view() , name='product_list'),
    path('page/<int:page>' , views.ProductList.as_view() , name='product_list'),
    path('detail/<slug:slug>' , views.ProductDetail.as_view() , name='product_detail'),
    path('category/<slug:slug>' , views.CategoryList.as_view() , name='category_list'),
    path('offer/' , views.OfferList.as_view() , name='offer_list'),
    path('privacy-policy/',views.privacy_policy,name="privacy-policy"),
    path ('search/' , views.SearchList.as_view() , name='search'),
]