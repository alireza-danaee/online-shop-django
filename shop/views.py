from django.shortcuts import render ,get_object_or_404
from django.views.generic import DetailView , ListView
from .models import Product , Category,Attribute
from cart.forms import CartAddProductForm
from django.db.models import Q
from comments.forms import CommentForm
from django.core.mail import EmailMessage
import json
import urllib
from django.conf import settings




class ProductList(ListView):
	queryset = Product.objects.all().order_by('status')
	template_name = 'product/home.html'
	paginate_by = 6
	def get_context_data(self , **kwargs):
		context = super().get_context_data(**kwargs)
		context['offers'] = Product.objects.filter(pishnahad=True).order_by('?')[:3]
		context['form'] = CartAddProductForm()
		return context
		

def product_detail(request , slug):
	product = get_object_or_404(Product , slug=slug)
	triats = Attribute.objects.filter(attribute=product)
	form = CartAddProductForm()
	product_comments = product.comments.filter(active=True).order_by('-created_on')
	if request.method == "POST":
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
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
				new_comment = comment_form.save(commit=False)
				new_comment.product = product
				new_comment.user = request.user
				new_comment.save()
				if request.user.email:
					mail_subject = "دریافت دیدگاه شما "
				message = """دیدگاه شما دریافت شد و به زودی به آن پاسخ میدهیم با تشکر از شما
				مگا گیم
				"""
				email = EmailMessage(
							mail_subject,
							message,
							to=[request.user.email]
				)
				email.send()
	else:
		comment_form = CommentForm()

	context = {
		"product":product,
		"form":form,
		"triats":triats,
		"comment_form":CommentForm(),
		"comments":product_comments,

	}
	return render(request , 'product/detail.html' , context)


class CategoryList(ListView):
	template_name = 'product/category_list.html'
	paginate_by = 6

	def get_queryset(self):
		global category
		slug = self.kwargs.get('slug')
		category = get_object_or_404(Category.objects.all() , slug=slug)
		return category.products.all()

	def get_context_data(self , **kwargs):
		context = super().get_context_data(**kwargs)
		context['offers'] = Product.objects.filter(pishnahad=True).order_by('?')[:3]
		context['form'] = CartAddProductForm()
		return context


class OfferList(ListView):
	queryset = Product.objects.filter(pishnahad = True)
	template_name = 'product/offer_list.html'


	def get_context_data(self , **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = CartAddProductForm()
		return context


class SearchList(ListView):
	template_name = 'product/search_list.html'
	paginate_by = 1
	def get_queryset(self): # new
		search = self.request.GET.get('q')
		product = Product.objects.filter(Q(name__icontains=search) | Q(description__icontains=search))
		return product

	def get_context_data(self , **kwargs):
		context = super().get_context_data(**kwargs)
		context['search'] = self.request.GET.get('q')
		context['form'] = CartAddProductForm()
		return context


def privacy_policy(request):
	return render(request , "product/privacy_policy.html")


