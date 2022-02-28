from django.shortcuts import render ,get_object_or_404
from django.views.generic import DetailView , ListView
from .models import Product , Category
from cart.forms import CartAddProductForm
# Create your views here.










class ProductList(ListView):
	queryset = Product.objects.all().order_by('status')
	template_name = 'product/home.html'
	paginate_by = 6
	def get_context_data(self , **kwargs):
		context = super().get_context_data(**kwargs)
		context['offers'] = Product.objects.filter(pishnahad=True).order_by('?')[:3]
		return context




class ProductDetail(DetailView):
	template_name = 'product/detail.html'
	def get_object(self):
		slug = self.kwargs.get('slug')
		product = get_object_or_404(Product.objects.all() , slug=slug)
		return product
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = CartAddProductForm()
		return context








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
		return context



class OfferList(ListView):
	queryset = Product.objects.filter(pishnahad = True)
	template_name = 'product/offer_list.html'


























	


	

