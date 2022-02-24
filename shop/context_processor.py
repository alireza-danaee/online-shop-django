from shop.models import Category

def render_request(request):
    ''' Access Request in templatetags
    '''
    
    category = Category.objects.all()
    
    return {
        'category' : category
    }