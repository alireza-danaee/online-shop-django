from django.shortcuts import render ,get_object_or_404
from django.views.generic import DetailView , ListView
from .models import Product
# Create your views here.


class ProductList(ListView):
	queryset = Product.objects.all()
	template_name = 'product/base.html'
	paginate_by = 3
	


