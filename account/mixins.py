from django.http import Http404


class AccessMixin():
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_superuser:
			self.fields = ['name','slug','description','image','image2','image3','image4','price','status','pishnahad','category']
		else:
			raise Http404
		return super().dispatch(request, *args, **kwargs)


class ProductAccessMixin():
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_superuser:
			self.fields = ['name','slug','description','image','image2','image3','image4','price','status','pishnahad','category']
		else:
			raise Http404
		return super().dispatch(request, *args, **kwargs)


class CategoryAccessMixin():
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_superuser:
			self.fields = ['name','slug']
		else:
			raise Http404
		return super().dispatch(request, *args, **kwargs)


class CouponAccessMixin():
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_superuser:
			self.fields = ['code','valid_from','valid_to','discount','active']
		else:
			raise Http404
		return super().dispatch(request, *args, **kwargs)


class OrderAccessMixin():
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_superuser:
			self.fields = ['first_name','last_name','email','address','postal_code','state' ,'city','paid','created','updated']
		else:
			raise Http404
		return super().dispatch(request, *args, **kwargs)