from django.db.transaction import commit
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from shop.models import Product
from cart.models import Cart
from django.contrib import messages
from cart.forms import OrderForm
from cart.models import Order,Order_item
import razorpay


# Create your views here.

class AddToCartView(View):
    def get(self, request, i):
        p = Product.objects.get(id=i)
        u = request.user
        try:
            c = Cart.objects.get(user=u, product=p)
            c.quantity += 1
            c.save()
        except Cart.DoesNotExist:
            c = Cart.objects.create(user=u, product=p, quantity=1)

        return redirect('cart:cartview')



class CartView(View):
    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total+=i.product.price*i.quantity
        context={'cart':c,'total':total}
        return render(request,'cart.html',context)


class CartDecrement(View):
    def get(self, request, i):
        p = Product.objects.get(id=i)
        u = request.user
        try:
            c = Cart.objects.get(user=u, product=p)
            if(c.quantity>1):
                c.quantity -= 1
                c.save()
            else:
                 c.delete()
        except:
              pass

        return redirect('cart:cartview')


class CartRemove(View):
    def get(self, request, i):
        p = Product.objects.get(id=i)
        u = request.user
        try:
            c = Cart.objects.get(user=u, product=p)
            c.delete()
        except:
            pass

        return redirect('cart:cartview')




def checkstock(c):
    for i in c:
        if i.product.stock < i.quantity:
            return False
    return True

import uuid
class CheckOutView(View):
    def post(self,request):
       form_instance=OrderForm(request.POST)
       if form_instance.is_valid():
           o=form_instance.save(commit=False)
           u=request.user
           o.user=u
           c=Cart.objects.filter(user=u)
           total=0
           for i in c:
               total+=i.product.price*i.quantity
           o.amount=total
           o.save()
           if(o.payment_method=="online"):
               client=razorpay.Client(auth=('rzp_test_ReUWG7E2XBz56n','NjTGjTcIHpYvYrwp7Y4OfFZ4'))
               print(client)
               response_payment=client.order.create(dict(amount=total*100,currency='INR'))
               print(response_payment)
               id=response_payment['id']
               o.order_id=id
               o.save()
               context={'payment':response_payment}
               return render(request, 'payment.html', context)
           else:
               o.is_ordered=True
               uid=uuid.uuid4().hex[:14]
               id='order_COD'+uid
               o.order_id=id
               o.save()
               for i in c:
                   items = Order_item.objects.create(order=o, product=i.product, quantity=i.quantity)
                   items.save()
                   items.product.stock -= items.quantity
                   items.product.save()

                   c.delete()
           return render(request,'payment.html')

    def get(self, request):
        u = request.user
        c = Cart.objects.filter(user=u)
        stock = checkstock(c)

        if stock:
            form_instance = OrderForm()
            context = {'form': form_instance}
            return render(request, 'checkout.html', context)
        else:
            messages.error(request, "Currently items not available. Can't place order. Please try again later!")
            return render(request, 'checkout.html')

from django.contrib.auth.models import User
from django.contrib.auth import login
@method_decorator(csrf_exempt,name="dispatch")
class Payment_success(View):
    def post(self,request,i):
        u=User.objects.get(username=i)
        login(request,u)
        response=request.POST
        print(response)
        id=response['razorpay_order_id']
        print(id)
        o=Order.objects.get(order_id=id)
        o.is_ordered=True
        o.save()
        c=Cart.objects.filter(user=u)
        for i in c:
            o=Order_item.objects.create(order=o,product=i.product,quantity=i.quantity)
            o.save()
            o.product.stock-=o.quantity
            o.product.save()

            c.delete()

        return render(request,'payment_success.html')

    
class OrderView(View):
    def get(self,request):
        u=request.user
        o=Order.objects.filter(user=u,is_ordered=True)
        context={'orders':o}
        return render(request,'orders.html',context)

