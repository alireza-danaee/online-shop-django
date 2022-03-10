from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


from .mixins import AccessMixin , ProductAccessMixin , CategoryAccessMixin,CouponAccessMixin
from shop.models import Product ,Category
from coupons.models import Coupons
from orders.models import Order , OrderItem
# Create your views here.







class Home(LoginRequiredMixin,ListView):
	queryset = Product.objects.all()
	template_name = 'registration/home.html'


# ---------------------- PRODUCTS -------------------------
class ProductListAdmin(LoginRequiredMixin,AccessMixin,ListView):
	queryset = Product.objects.all()
	template_name = 'registration/product/product_list.html'


class ProductCreate(LoginRequiredMixin,ProductAccessMixin,CreateView):
	model = Product
	template_name = 'registration/product/product_create_update.html'


class ProductUpdate(LoginRequiredMixin,ProductAccessMixin,UpdateView):
	model = Product
	template_name = 'registration/product/product_create_update.html'


class ProductDelete(ProductAccessMixin,DeleteView):
	model = Product
	success_url = reverse_lazy('account:product-list')
	template_name = 'registration/product/product_delete.html'


# ---------------------- CATEGORIES -------------------------

class CategoryListAdmin(LoginRequiredMixin,CategoryAccessMixin,ListView):
	queryset = Category.objects.all()
	template_name = 'registration/category/category_list.html'


class CategoryCreate(LoginRequiredMixin,CategoryAccessMixin,CreateView):
	model = Category
	template_name = 'registration/category/category_create_update.html'


class CategoryUpdate(LoginRequiredMixin,CategoryAccessMixin,UpdateView):
	model = Category
	template_name = 'registration/category/category_create_update.html'


class CategoryDelete(ProductAccessMixin,DeleteView):
	model = Category
	success_url = reverse_lazy('account:category-list')
	template_name = 'registration/category/category_delete.html'



class CouponListAdmin(LoginRequiredMixin,CouponAccessMixin,ListView):
	queryset = Coupons.objects.all()
	template_name = 'registration/coupon/coupon_list.html'


class CouponCreate(LoginRequiredMixin,CouponAccessMixin,CreateView):
	model = Coupons
	template_name = 'registration/coupon/coupon_create_update.html'

	



class OrderList(LoginRequiredMixin,ListView):
	queryset = Order.objects.all()
	template_name = 'registration/order/order_list.html'


def order_detail(request ,pk):
	order = OrderItem.objects.filter(user_id=request.user.id)
	context = {
		'order_detail':order,
	}
	return render(request,'registration/order/order_detail.html',context)



