from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import OrderItem





@receiver(post_save,sender=OrderItem)
def inventory_product(sender,instance,created,**kwargs):
    if created:
        instance.product.Inventory -= instance.quantity
        if instance.product.Inventory == 0:
            instance.product.status = 'u'
            instance.product.save()
        instance.product.save()
                                          
    
