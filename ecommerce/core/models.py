from audioop import reverse
from msilib.schema import SelfReg
from django.db import models 
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):

    user=models.OneToOneField(User,null=False,blank=False,on_delete=models.CASCADE)


    phone_field =models.CharField(max_length=12,blank=False)


    def __str__(self):
        return self.user.username

# catagoty
class Catagory(models.Model):
    catagory_name=models.CharField(max_length=200)
    def __str__(self):
        return self.catagory_name
    

class Product(models.Model):
    name=models.CharField(max_length=100)
    catagory=models.ForeignKey('Catagory',on_delete=models.CASCADE)
    desc=models.TextField()
    original_price=models.IntegerField(default=0.0)
    selling_price=models.FloatField(default=0.0)
    product_available_count=models.IntegerField(default=0)
    img=models.ImageField(upload_to='images/')
    
    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart",kwargs={
            "pk":self.pk
        })
    def __str__(self):
        return self.name
    
class OrderItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=False)


    def __srt__(self):
        return f"{self.quantity} of {self.product.name}"
    
    def get_total_item_selling_price(self):
        return self.quantity * self.product.selling_price
    
    def get_final_selling_price(self):
        return self.get_total_item_selling_price()
    
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)
    order_id=models.CharField(max_length=100,unique=True,default=None,blank=True,null=True)
    datetime_ofpayment=models.DateTimeField(auto_now_add=True)
    order_delivered=models.BooleanField(default=False)
    order_received=models.BooleanField(default=False)

    def save(self,*args,**kwargs):
        if self.order_id is None and self.datetime_ofpayment and self.id:
            self.order_id=self.datetime_ofpayment.strftime('PAY2ME%Y%m%dODR')+str(self.id)
        
        return super().save(*args,**kwargs)
    
    def __str__(self):
        return self.user.username
    
    def get_total_selling_price(self):
        total=0
        for order_item in self.items.all():
            total+=order_item.get_final_selling_price()
        return total
    
    def get_total_count(Self):
        order=Order.objects.get(pk=SelfReg.pk)
        return order.items.count()
    
#adress check
class CheckoutAddress(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    street_address=models.TextField()
    district=models.CharField(max_length=20)
    pin_code=models.CharField(max_length=6)

    def __str__(self):
        return self.user.username