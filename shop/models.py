from django.db import models
from django.urls import reverse
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name="نام دسته بندی")
    slug = models.SlugField(max_length=100 , unique=True ,verbose_name="آدرس دسته بندی")


    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return self.name





class Product(models.Model):
    CHOOSE_STATUS = (
        ('u' , 'ناموجود'),         # unavailble
        ('a' , 'موجود'),           # available
        ('c' , 'قابل سفارش'),      # Customizable
        
    )
    name = models.CharField(max_length=100,verbose_name="نام محصول")
    slug = models.SlugField(max_length=100 , unique=True ,verbose_name="آدرس محصول")
    description = models.TextField(verbose_name="توضیحات محصول")
    image = models.ImageField(upload_to='products/%Y/%m/%d',verbose_name="تصویر اصلی محصول")
    image2 = models.ImageField(upload_to='products/%Y/%m/%d',verbose_name="تصویر جانبی 1 محصول")
    image3 = models.ImageField(upload_to='products/%Y/%m/%d',verbose_name="تصویر جانبی 2 محصول")
    image4 = models.ImageField(upload_to='products/%Y/%m/%d',verbose_name="تصویر جانبی 3 محصول")
    price = models.PositiveIntegerField(verbose_name="قیمت محصول")
    status = models.CharField(choices=CHOOSE_STATUS , max_length=1 , verbose_name='وضعیت')
    pishnahad = models.BooleanField(default=False , verbose_name="پیشنهاد شده")
    category = models.ForeignKey(Category , on_delete=models.CASCADE , verbose_name="دسته بندی", related_name="products") 
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('account:home')
