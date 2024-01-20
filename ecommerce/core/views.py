from datetime import datetime, timezone
from itertools import product
from django.shortcuts import render,redirect
from core.forms import CheckoutForm, ProductForm ,CheckoutForm
from django.contrib import messages
from core.models import *
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
 #Create your views here.
def index(request):
    products =Product.objects.all()
    return render(request,'core/index.html',{'products':products})

def orderlist(request):
   if Order.objects.filter(user=request.user,ordered=False).exists():
      order=Order.objects.get(user=request.user,ordered=False)
      return render(request,'core/orderlist.html',{'order':order})
   return render(request,'core/orderlist.html',{'message':"Your Cart Is Empty"})


def add_product(request):
    if request.method =='POST':
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
          print('True')
          form.save()
          print("data saved successfully")
          return redirect('add_product')
        else:
          print("Not working")
          messages.info(request,"products is not added, try again")  

    else:
        form=ProductForm()
    return render(request,'core/add_product.html',{'form':form})

def product_desc(request,pk):
   product=Product.objects.get(pk=pk)
   return render(request,'core/product_desc.html',{'product':product})

def add_to_cart(request,pk):
   #get the some id
   product=Product.objects.get(pk=pk)

#create order products
   order_item,created=OrderItem.objects.get_or_create(
      product=product,
      user=request.user,
      ordered=False,
   )
#quary set
   order_qs=Order.objects.filter(user=request.user,ordered=False)
   if order_qs.exists():
      order=order_qs[0]
      if order.items.filter(product__pk = pk).exists():
         order_item.quantity +=1
         order_item.save()
         messages.info(request,"Added Quantity Item")
         return redirect("product_desc",pk=pk)
      else:
         order.items.add(order_item)
         messages.info(request,"Item Added To Cart")
         return redirect("product_desc",pk=pk)
   else:
      ordered_date=datetime.now(timezone.utc)
      order=Order.objects.create(user=request.user,ordered_date=ordered_date)
      order.items.add(order_item)
      messages.info(request,"Item Added to Cart")
      return redirect("product_desc",pk=pk)

def add_item(request,pk):

          #get the some id
   product=Product.objects.get(pk=pk)

#create order products
   order_item,created=OrderItem.objects.get_or_create(
      product=product,
      user=request.user,
      ordered=False,
   )
#quary set
   order_qs=Order.objects.filter(user=request.user,ordered=False)
   if order_qs.exists():
      order=order_qs[0]
      if order.items.filter(product__pk = pk).exists():
         if order_item.quantity < product.product_available_count:
           order_item.quantity +=1
           order_item.save()
           messages.info(request,"Added Quantity Item")
           return redirect("orderlist")
         else:
            messages.info(request,"Sorry Product is out of Stack")
            return redirect("orderlist")
      else:
         order.items.add(order_item)
         messages.info(request,"Item Added To Cart")
         return redirect("product_desc",pk=pk)
   else:
      ordered_date=datetime.now(timezone.utc)
      order=Order.objects.create(user=request.user,ordered_date=ordered_date)
      order.items.add(order_item)
      messages.info(request,"Item Added to Cart")
      return redirect("product_desc",pk=pk)

def remove_item(request,pk,):
   item=get_object_or_404(Product,pk=pk)
   order_qs=Order.objects.filter(
      user=request.user,
      ordered=False,
   )
   if order_qs.exists():
      order=order_qs[0]
      if order.items.filter(product__pk=pk).exists():
         order_item=OrderItem.objects.filter(
            product=item,
            user=request.user,
            ordered=False,
         )[0]
         if order_item.quantity >1:
            order_item.quantity-=1
            order_item.save()
         else:
            order_item.delete()
         messages.info(request,"Item Quantity was Updated")
         return redirect("orderlist")
      else:
         messages.info(request,"this is not in your cart")
         return redirect("orderlist")
   else:
      messages.info(request,"You Do Not have any Order")
      return redirect("orderlist")

def checkout(request):
   if CheckoutAddress.objects.filter(user=request.user).exists():
      return render(request,'core/checkout.html',{" payment_allow":"allow"})
   if request.method =='POST':
      form=CheckoutForm(request.POST)
      try:
         if form.is_valid():
            street_address=form.cleaned_data.get('street_address')
            district=form.cleaned_data.get('district')
            pin_code=form.cleaned_data.get('pin')

            checkout_address=CheckoutAddress(
               user=request.user,
               street_address=street_address,
               district=district,
               pin_code=pin_code,
            )
            checkout_address.save()
            print("It should render the sumary page")
            return render(request,'core/checkout.html',{"payment_allow":"allow"})
      except Exception as e:
         messages.warning(request,"Failed Checkout")
         return redirect('checkout')
   else:
      form=CheckoutForm()
      return render(request,'core/checkout.html',{'form':form})
   
def invoice(request):
   return render(request,"invoice/invoice.html")