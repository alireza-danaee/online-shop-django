from django import template
from shop.models import Category 


register = template.Library()






@register.inclusion_tag('product/partials/category_navbar.html')
def category_navbar():
    return {
        'category': Category.objects.all()
    }




