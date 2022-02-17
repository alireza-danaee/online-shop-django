from django.shortcuts import render ,get_object_or_404
from django.views.generic import DetailView , ListView
from .models import Product , Category
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
# Create your views here.







def product_list(request,page=1):
		Model_one = Product.objects.all()
		paginator = Paginator(Model_one, 6)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)

		Model_two = Product.objects.filter(pishnahad=True)
		paginator = Paginator(Model_two, 3)
		page = request.GET.get('page2')
		try:
			Model_two = paginator.page(page)
		except PageNotAnInteger:
			Model_two = paginator.page(1)
		except EmptyPage:
			Model_two = paginator.page(paginator.num_pages)

		context = {'page_obj': page_obj, 'Model_two': Model_two}
		return render(request, 'product/home.html', context)








def category_list(request,slug):
		category = get_object_or_404(Category , slug=slug)
		products = Product.objects.all()
		products = products.filter(category=category)
		paginator = Paginator(products, 6)
		page = request.GET.get('page1')
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			products = paginator.page(1)
		except EmptyPage:
			products = paginator.page(paginator.num_pages)

		Model_two = Product.objects.filter(pishnahad=True)
		paginator = Paginator(Model_two, 3)
		page = request.GET.get('page2')
		try:
			Model_two = paginator.page(page)
		except PageNotAnInteger:
			Model_two = paginator.page(1)
		except EmptyPage:
			Model_two = paginator.page(paginator.num_pages)

		context = {'category': products, 'Model_two': Model_two}
		return render(request, 'product/category_list.html', context)







	


	


