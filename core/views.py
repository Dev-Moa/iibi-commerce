from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from core.forms import CustomUserCreationForm, ProductForm
from .models import Category, CustomUser, Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class IndexView(View):
    def get(self,request):
        products = Product.objects.all()
        latest_products = products.order_by("-date")[:2]
        return render(request,"core/index.html",{"products":products,"latest_products":latest_products})

class SignUpView(View):
    def get(self,request):
        form = CustomUserCreationForm
        return render(request,"registration/signup.html",{"form":form,"error":False})
    def post(self,request):
        form = CustomUserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
        form = UserCreationForm
        return render(request,"registration/signup.html",{"form":form,"error":True})
    
class CreateProduct(LoginRequiredMixin,View):
    def get(self,request):
        form = ProductForm
        return render(request,"core/product/add.html",{"form":form})
    def post(self,request):
        user = request.user
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():   
            form = form.save(commit=False)      
            form.owner = user
            form.save()
            return redirect('/products')
        form = ProductForm
        return render(request,"core/product/add.html",{"form":form,"eror":True})
  
class RetrieveProduct(View):

    categories = Category.objects.all()
    def get(self,request):
        products = Product.objects.all()
        categories = self.categories
        return render(request,"core/product/list.html",{"products":products,"categories":categories})
    def post(self,request):
        q= request.POST["q"]
        r = self.categories.filter(category_name=q)
        return
        pass

class DetailProduct(View):
    def get(self,request,id):
        product = Product.objects.get(id=id)
        prod_id = product.pk
        owner = product.owner == request.user
        carts = request.session.get('carts')
        is_cart = False
        if carts is not None :
            is_cart = int(prod_id) in carts 
        return render(request,"core/product/detail.html",{"is_cart":is_cart,"product":product,"owner":owner})
 
class UpdateProduct(LoginRequiredMixin,View):
    def get(self,request,id):
        product = Product.objects.get(id=id)
        if request.user == product.owner:
            form = ProductForm(request.POST or None,instance=product)
            return render(request,"core/product/update.html",{"form":form,"product":product})
        return redirect('/')
    def post(self,request,id):
        product = Product.objects.get(id=id)
        form = ProductForm(request.POST or None,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect('/products')
        product = Product.objects.get(id=id)
        form = ProductForm(request.POST or None,instance=product)
        return render(request,"core/product/update.html",{"form":form,"product":product})
        
class DeleteProduct(LoginRequiredMixin,View):
    
    def get(self,request,id):
        product = Product.objects.get(id=id)
        return render(request,"core/product/delete.html",{"product":product})
        
    def post(self,request,id):
        product = Product.objects.get(id=id)
        product.delete()
        return redirect('/products')

class CategoryDetail(View):
    def get(self,request,name):
        category = Category.objects.get(category_name=name)
        category_products = category.products.all()
        return render(request,"core/product/category_list.html",{"category":category,"products":category_products})
    
class UserProfile(View):
    def get(self,request,id):
        product =  Product.objects.get(id=id)
        owner = product.owner
        products = Product.objects.filter(owner = owner)
        return render(request,"core/profiles/profile.html",{"owner":owner,"products":products})

class AddToCart(View):
    def get(self,request):
        carts = request.session.get('carts')

        context = {}

        if carts is None:
            context["carts"] = []
            context["has_carts"] = False
        else:
            product = Product.objects.filter(id__in=carts)
            context["carts"] = product
            context["has_carts"] = True
        return render(request,"core/product/cart-list.html",context)

    def post(self,request):
        product_id = request.POST['product_id']
        carts = request.session.get('carts')
        if carts is None:
            carts = []
        if product_id not in carts:
            carts.append(int(product_id))
            request.session['carts'] = carts
        return redirect('/')

        

class RemoveCart(LoginRequiredMixin,View):
    def get(self,request,id):
        product = Product.objects.get(id=id)
        return render(request,"core/product/remove-cart.html",{"product":product})

    def post(self,request,id):
        product = Product.objects.get(id=id)
        carts = request.session.get("carts")
        carts.remove(int(product.id))
        request.session["carts"] = carts
        return redirect(reverse("home"))

