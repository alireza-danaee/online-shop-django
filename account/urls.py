from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.urls import reverse_lazy




app_name = 'account'

urlpatterns = [
    #--------------------------AUTH--------------------------------
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', views.MyPasswordChangeView.as_view(template_name='registration/password/password_change_form.html',success_url=reverse_lazy('account:password_change_done')), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password/password_change_done.html'), name='password_change_done'),
    path('password_reset/', views.password_reset_request , name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password/password_reset_confirm.html",success_url=reverse_lazy('account:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password/password_reset_complete.html'), name='password_reset_complete'),  
]


urlpatterns += [
    path ('' ,views.Home.as_view() , name = 'home'),
    #----------------------PRODUCTS----------------------
    path ('product/list' ,views.ProductListAdmin.as_view() , name = 'product-list'),
    path ('product/create/' ,views.ProductCreate.as_view() , name = 'product-create'),
    path ('product/update/<int:pk>' ,views.ProductUpdate.as_view() , name = 'product-update'),
    path ('product/delete/<int:pk>' ,views.ProductDelete.as_view() , name = 'product-delete'),

    #----------------------CATEGORIES----------------------
    path ('category/list/' ,views.CategoryListAdmin.as_view() , name = 'category-list'),
    path ('category/create/' ,views.CategoryCreate.as_view() , name = 'category-create'),
    path ('category/update/<int:pk>' ,views.CategoryUpdate.as_view() , name = 'category-update'),
    path ('category/delete/<int:pk>' ,views.CategoryDelete.as_view() , name = 'category-delete'),


    path ('coupon/list/' ,views.CouponListAdmin.as_view() , name = 'coupon-list'),
    path ('coupon/create/' ,views.CouponCreate.as_view() , name = 'coupon-create'),
    #-----------------------ORDERS---------------------------
    path ('order/list/' ,views.OrderList.as_view() , name = 'order-list'),
    path ('order/history/' ,views.order_history_user , name = 'order-history-user'),
    path ('order/history/<int:order_user_id>/' ,views.order_history_admin , name = 'order-history-admin'),

    path ('profile/' ,views.Profile.as_view() , name = 'profile'),
]
