from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import AccessMixin , ProductAccessMixin , CategoryAccessMixin,CouponAccessMixin
from shop.models import Product ,Category
from coupons.models import Coupons
from orders.models import Order , OrderItem
from account.models import User
from django.http import HttpResponse
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage






class Home(LoginRequiredMixin,ListView):
	queryset = Product.objects.all()
	template_name = 'registration/home.html'
	def get_context_data(self , **kwargs):
		context = super().get_context_data(**kwargs)
		context['all_users'] =  User.objects.all().count()
		context['all_orders'] =  Order.objects.all().count()
		context['all_products'] =  Product.objects.all().count()
		context['all_coupons'] =  Coupons.objects.all().count()
		return context


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
	def get_context_data(self , **kwargs):
		context = super().get_context_data(**kwargs)
		context['order_id'] = OrderItem.objects.filter(user_id=self.request.user.id)
		return context


def order_history_user(request ):
	order = OrderItem.objects.filter(user_id=request.user.id)
	context = {
		'order_detail':order,
	}
	return render(request,'registration/order/order_detail.html',context)

		
def order_history_admin(request ,id ):
	order = OrderItem.objects.filter(user_id=id)
	context = {
		'order_detail':order,
	}
	return render(request,'registration/order/order_history_admin.html',context)
	

class Profile(UpdateView):
	model = User
	fields = ['username','first_name','last_name','email']
	template_name = 'registration/profile.html'
	success_url = reverse_lazy('account:profile')
	def get_object(self):
		return User.objects.get(pk = self.request.user.pk)


class Register(CreateView):
	form_class = SignupForm
	template_name = 'registration/register.html'
	def form_valid(self , form):
		user = form.save(commit=False)
		user.is_active = False
		user.save()
		current_site = get_current_site(self.request)
		mail_subject = 'فعالسازی حساب شما در سایت مگاگیم'
		message = render_to_string('registration/acc_active_email.html', {
			'user': user,
			'domain': current_site.domain,
			'uid':urlsafe_base64_encode(force_bytes(user.pk)),
			'token':account_activation_token.make_token(user),
		})
		to_email = form.cleaned_data.get('email')
		email = EmailMessage(
					mail_subject, message, to=[to_email]
		)
		email.send()
		return HttpResponse('لطفا آدرس ایمیل خود را برای تکمیل ثبت نام تایید کنید')


def activate(request, uidb64, token):
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		# return redirect('home')
		return HttpResponse('باتشکر از شما برای تایید ایمیل  اکنون میتوانید به حساب کاربری خود وارد شوید <a href="/login">ورود </a>')
	else:
		return HttpResponse('لینک فعال سازی نامعتبر است!')



