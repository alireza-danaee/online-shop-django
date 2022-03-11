# The views used below are normally mapped in the AdminSite instance.
# This URLs file is used to provide a reliable view deployment for test purposes.
# It is also provided as a convenience to those who want to deploy these URLs
# elsewhere.

from django.contrib.auth import views
from django.urls import path
from .views import (
    CategoryDelete, CategoryUpdate, 
    CategoryCreate, CategoryListAdmin,
    CouponListAdmin, CouponCreate,
    ProductDelete, ProductListAdmin,
    ProductCreate, ProductUpdate, 
    Home,OrderList,
    order_detail,Profile
)





app_name = 'account'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

#     path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
#     path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

#     path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
#     path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#     path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]




urlpatterns += [
    path ('' ,Home.as_view() , name = 'home'),
    #----------------------PRODUCTS----------------------
    path ('product/list' ,ProductListAdmin.as_view() , name = 'product-list'),
    path ('product/create/' ,ProductCreate.as_view() , name = 'product-create'),
    path ('product/update/<int:pk>' ,ProductUpdate.as_view() , name = 'product-update'),
    path ('product/delete/<int:pk>' ,ProductDelete.as_view() , name = 'product-delete'),

    #----------------------CATEGORIES----------------------
    path ('category/list/' ,CategoryListAdmin.as_view() , name = 'category-list'),
    path ('category/create/' ,CategoryCreate.as_view() , name = 'category-create'),
    path ('category/update/<int:pk>' ,CategoryUpdate.as_view() , name = 'category-update'),
    path ('category/delete/<int:pk>' ,CategoryDelete.as_view() , name = 'category-delete'),


    path ('coupon/list/' ,CouponListAdmin.as_view() , name = 'coupon-list'),
    path ('coupon/create/' ,CouponCreate.as_view() , name = 'coupon-create'),

    path ('order/list/' ,OrderList.as_view() , name = 'order-list'),
    path ('order/detail/' ,order_detail , name = 'order-detail'),

    path ('profile/' ,Profile.as_view() , name = 'profile'),
]
