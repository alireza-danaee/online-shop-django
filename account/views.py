from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import AccessMixin , ProductAccessMixin , CategoryAccessMixin,CouponAccessMixin
from shop.models import Product ,Category
from coupons.models import Coupons
from orders.models import Order , OrderItem
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
import json
import urllib
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView ,PasswordChangeView
from account.forms import MyAuthenticationForm , MyPasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query_utils import Q





class Home(LoginRequiredMixin,ListView):
	queryset = Product.objects.all()
	template_name = 'registration/home.html'
	def get_context_data(self , **kwargs):
		context = super().get_context_data(**kwargs)
		context['all_users'] =  get_user_model().objects.all().count()
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

# ---------------------- COUPON -------------------------

class CouponListAdmin(LoginRequiredMixin,CouponAccessMixin,ListView):
	queryset = Coupons.objects.all()
	template_name = 'registration/coupon/coupon_list.html'


class CouponCreate(LoginRequiredMixin,CouponAccessMixin,CreateView):
	model = Coupons
	template_name = 'registration/coupon/coupon_create_update.html'


class OrderList(LoginRequiredMixin,ListView):
	queryset = Order.objects.all()
	template_name = 'registration/order/order_list.html'
	

def order_history_user(request ):
	order = OrderItem.objects.filter(user_id=request.user.id)
	context = {
		'order_detail':order,
	}
	return render(request,'registration/order/order_detail.html',context)

# ---------------------- AUTH -------------------------

class Profile(UpdateView):
	model = get_user_model()
	fields = ['username','first_name','last_name','email']
	template_name = 'registration/profile.html'
	success_url = reverse_lazy('account:profile')
	def get_object(self):
		return get_user_model().objects.get(pk = self.request.user.pk)


class MyLoginView(LoginView):
	form_class = MyAuthenticationForm


class Register(CreateView):
	form_class = SignupForm
	template_name = 'registration/register.html'
	
	def form_valid(self , form):
		''' Begin reCAPTCHA validation '''
		recaptcha_response = self.request.POST.get('g-recaptcha-response')
		url = 'https://www.google.com/recaptcha/api/siteverify'
		values = {
			'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
			'response': recaptcha_response
		}
		data = urllib.parse.urlencode(values).encode()
		req =  urllib.request.Request(url, data=data)
		response = urllib.request.urlopen(req)
		result = json.loads(response.read().decode())
		''' End reCAPTCHA validation '''
		if result['success']:
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
			return render(self.request ,'registration/complete_email_register.html')
		else:
			messages.error(self.request, 'Invalid reCAPTCHA. Please try again.')
		return redirect("register")

def activate(request, uidb64, token):
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = get_user_model().objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		
		return render(request ,'registration/after_confirm_email_register.html')
	else:
		return HttpResponse('لینک فعال سازی نامعتبر است!')


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			''' Begin reCAPTCHA validation '''
			recaptcha_response = request.POST.get('g-recaptcha-response')
			url = 'https://www.google.com/recaptcha/api/siteverify'
			values = {
				'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
				'response': recaptcha_response
			}
			data = urllib.parse.urlencode(values).encode()
			req =  urllib.request.Request(url, data=data)
			response = urllib.request.urlopen(req)
			result = json.loads(response.read().decode())
			''' End reCAPTCHA validation '''
			if result['success']:
				data = password_reset_form.cleaned_data['email']
				associated_users = get_user_model().objects.filter(Q(email=data))
				if associated_users.exists():
					for user in associated_users:
						subject = "Password Reset Requested"
						email_template_name = "registration/password/password_reset_email.txt"
						c = {
						"email":user.email,
						'domain':'127.0.0.1:7000',
						'site_name': 'مگا گیم',
						"uid": urlsafe_base64_encode(force_bytes(user.pk)),
						"user": user,
						'token': default_token_generator.make_token(user),
						'protocol': 'http',
						}
						email = render_to_string(email_template_name, c)
						try:
							send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
						except BadHeaderError:
							return HttpResponse('Invalid header found.')
						return redirect ("account:password_reset_done")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="registration/password/password_reset.html", context={"password_reset_form":password_reset_form})


class MyPasswordChangeView(PasswordChangeView):
	form_class = MyPasswordChangeForm





