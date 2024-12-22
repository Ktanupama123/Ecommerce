from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import ProductForm
from .models import CustomUser,Product
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.contrib import messages
# import datetime
from django.contrib.auth.decorators import login_required
import os
# from dotenv import load_dotenv
# load_dotenv()
# Create your views here.
def add_product(request):
    form = ProductForm()
    if request.method =="POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('addproduct')
        else:
            form = ProductForm()
    context = {
        "form":form
    }
    return render(request,"addproducts.html",context)
def signupview(request):
    errors={}
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        print(username,"llllllllllllll")
        print(email)
        print(password)
        print(confirm_password)
        if CustomUser.objects.filter(username=username).exists():
            errors['username']="Username is already exists"

        if CustomUser.objects.filter(email=email).exists():
            errors["email"]="email is already taken"
            # messages.error(request,'email is already taken') 
        if password!=confirm_password:
            errors["confirm_password"]="password do not match!"
            # messages.error(request,'password is not same')
            # return redirect('signup')
        if errors:
            return render(request,'signup.html',{'errors':errors})
        user= CustomUser.objects.create_user(email=email,username=username,password=password)
        user.set_password(password)
        user.save()
        return redirect('login')
    return render(request,'signup.html')

def signinview(request):
    if request.method=='POST':
        errors = {}
        user_name=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=user_name,password=password)
        if user is  None :
            errors["user"]="User not exist"
        if errors:
            return render(request,"signin.html",{'errors':errors})
        else:
            login(request,user)
            messages.success(request,'Login successfull')
            return redirect('addproduct')
    return render(request,'signin.html')
def signoutview(request):   
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')
@login_required(login_url='login')

def productlist(request):
    pdt = None
    try:
        searching = request.GET.get('query', '')
        if searching:
            pdt = Product.objects.filter(productname__icontains=searching)
        else:
            pdt = Product.objects.all()
        return render(request, 'productlist.html', {'products': pdt})
    except Exception:
        return render(request, 'productlist.html', {'products': pdt})

def product_delete(request,id):
    product=Product.objects.get(id=id)
    product.delete()
    messages.success(request,'Product deleted successfully')
    return redirect('productlist')
def product_edit(request,id):
    product=Product.objects.get(id=id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('productlist')
    else:
        form = ProductForm(instance=product)
    return render(request,'editproduct.html',{'product':product,'form':form})