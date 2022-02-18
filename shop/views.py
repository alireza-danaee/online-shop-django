from django.shortcuts import render ,get_object_or_404
from django.views.generic import DetailView , ListView
from .models import Product , Category
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
# Create your views here.










class ProductList(ListView):
	queryset = Product.objects.all()
	template_name = 'product/home.html'
	paginate_by = 6
	def get_context_data(self , **kwargs):
		context = super().get_context_data(**kwargs)
		context['offers'] = Product.objects.filter(pishnahad=True).order_by('?')[:3]
		return context












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







	


	


