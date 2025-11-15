from django.shortcuts import render,redirect
from django.views import View
from shop.models import Category



class CategoryView(View):
    def get(self,request):
      c=Category.objects.all()
      context={'categories':c}
      return render(request,'category.html',context)


class ProductView(View):
    def get(self,request,i):
        c = Category.objects.get(id=i)
        context = {'category': c}
        return render(request,'products.html',context)


from shop.models import Product
class ProductDetailView(View):
    def get(self, request,i):
        p=Product.objects.get(id=i)
        context={'product':p}
        return render(request, 'productdetail.html',context)



from shop.forms import SignupForm,LoginForm
class RegisterView(View):
        def post(self, request):
            form_instance = SignupForm(request.POST)
            context = {'form': form_instance}
            if form_instance.is_valid():
                form_instance.save()
                return redirect('shop:login')
            else:
                print('error')
                return render(request, 'register.html', context={'form': form_instance})

        def get(self, request):
            form_instance = SignupForm()
            context = {'form': form_instance}
            return render(request, 'register.html', context)


from django.contrib.auth import login, authenticate, logout

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views import View
from shop.forms import LoginForm


class LoginView(View):
    def post(self, request):
        form_instance = LoginForm(request.POST)
        context = {'form': form_instance}
        if form_instance.is_valid():
            U = form_instance.cleaned_data['username']
            P = form_instance.cleaned_data['password']
            user = authenticate(username=U, password=P)

            if user:
                login(request, user)
                if user.is_superuser:

                    return redirect('/admin/')
                else:

                    return redirect('shop:category')
            else:
                print("invalid user credentials")
                return render(request, 'login.html', context)
        else:
            return render(request, 'login.html', context)

    def get(self, request):
        form_instance = LoginForm()
        context = {'form': form_instance}
        return render(request, 'login.html', context)

class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('shop:login')



from shop.forms import CategoryForm,ProductForm,StockForm
from django.views import View
from shop.forms import CategoryForm

class AddCategoryView(View):
        def get(self, request):
            form_instance = CategoryForm()
            return render(request, 'addcategory.html', {'form': form_instance})

        def post(self, request):
            form_instance = CategoryForm(request.POST, request.FILES)
            if form_instance.is_valid():
                form_instance.save()
                return redirect('shop:category')
            else:
                print("Form is invalid")
                return render(request, 'addcategory.html', {'form': form_instance})

class AddProductView(View):
    def get(self, request):
        form_instance = ProductForm()
        return render(request, 'addproduct.html', {'form': form_instance})

    def post(self, request):
        form_instance = ProductForm(request.POST, request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:category')
        else:
            print("Form is invalid")
            return render(request, 'addproduct.html', {'form': form_instance})



class AddStockView(View):
    def get(self, request,i):
        p=Product.objects.get(id=i)
        form_instance = StockForm(instance=p)
        return render(request, 'addstock.html', {'form': form_instance})

    def post(self, request,i):
        p = Product.objects.get(id=i)
        form_instance = StockForm(request.POST, instance=p)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:category')
        else:
            print("Form is invalid")
            return render(request, 'addstock.html', {'form': form_instance})
