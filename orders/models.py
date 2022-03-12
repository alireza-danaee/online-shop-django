from django.db import models
from shop.models import Product
from account.models import User
# Create your models here.




class Order(models.Model):
    STATE_CHOICES = (
        ('آذربایجان شرقی','آذربایجان شرقی'),
        ('آذربایجان غربی','آذربایجان غربی'),
        ('اردبیل','اردبیل'),
        ('اصفهان','اصفهان'),
        ('البرز','البرز'),
        ('ایلام','ایلام'),
        ('بوشهر','بوشهر'),
        ('تهران','تهران'),
        ('خراسان جنوبی','خراسان جنوبی'),
        ('خراسان رضوی','خراسان رضوی'),
        ('خراسان شمالی','خراسان شمالی'),
        ('خوزستان','خوزستان'),
        ('زنجان','زنجان'),
        ('سمنان','سمنان'),
        ('سیستان و بلوچستان','سیستان و بلوچستان'),
        ('فارس','فارس'),
        ('قزوین','قزوین'),
        ('قم','قم'),
        ('لرستان','لرستان'),
        ('مازندران','مازندران'),
        ('مرکزی','مرکزی'),
        ('هرمزگان','هرمزگان'),
        ('همدان','همدان'),
        ('چهارمحال و بختیاری','چهارمحال و بختیاری'),
        ('کردستان','کردستان'),
        ('کرمان','کرمان'),
        ('کرمانشاه','کرمانشاه'),
        ('کهگیلویه و بویراحمد','کهگیلویه و بویراحمد'),
        ('گلستان','گلستان'),
        ('گیلان','گیلان'),
        ('یزد','یزد'),
        
        
    )
       
    first_name = models.CharField(max_length=100 , verbose_name='نام')
    last_name = models.CharField(max_length=100 ,verbose_name='نام خانوادگی')
    email = models.EmailField(verbose_name='ایمیل')
    phone = models.CharField(max_length=11 , verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')
    city = models.CharField(max_length=100,verbose_name='شهر')
    postal_code = models.CharField(max_length=10,verbose_name='کد پستی')
    created = models.DateTimeField(auto_now_add=True , verbose_name='تاریخ ثبت')
    updated = models.DateTimeField(auto_now=True , verbose_name='تاریخ بروزرسانی')
    paid = models.BooleanField(default=False ,verbose_name='پرداخت شده')
    state = models.CharField(max_length=100 , choices=STATE_CHOICES , verbose_name='استان')
    description_user = models.TextField(null=True, blank=True , verbose_name='توضیحات کاربر')

    
    class Meta:
        ordering = ('-created',)
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'




class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE,verbose_name='سفارش')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE,verbose_name='محصول')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    quantity = models.PositiveIntegerField(default=1 , verbose_name='تعداد')

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = 'سفارش کالا'
        verbose_name_plural = 'سفارشات کالا'






