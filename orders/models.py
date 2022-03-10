from django.db import models
from shop.models import Product
from account.models import User
# Create your models here.




class Order(models.Model):
    STATE_CHOICES = (
        ('خراسان' , 'خراسان',),
        ('تهران' , 'تهران'),
        ('اصفهان' , 'اصفهان'),
    )
       
    first_name = models.CharField(max_length=100 , verbose_name='نام')
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    state = models.CharField(max_length=100 , choices=STATE_CHOICES)


    class Meta:
        ordering = ('-created',)




class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity






