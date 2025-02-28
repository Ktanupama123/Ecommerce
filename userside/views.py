from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import ProductForm
from .models import CustomUser,Product,Cart
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.contrib import messages
# import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
import os
# from dotenv import load_dotenv
# load_dotenv()
# Create your views here.
@login_required(login_url='login')
def add_product(request):
    if not request.user.is_staff:  
        return HttpResponseForbidden("You are not authorized to view this page.")
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
    errors = {}
    logged_in_user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        print(username, "llllllllllllll")
        print(email)
        print(password)
        print(confirm_password)

        # If the logged-in user is admin, allow 'admin' as username and 'admin@gmail.com' as email
        if logged_in_user.is_staff:  # Admin is logged in
            if username == "admin":
                username = "admin"  # Allow admin username
            if email == "admin@gmail.com":
                email = "admin@gmail.com"  # Allow admin email

        # Check if the username already exists (except admin)
        if CustomUser.objects.filter(username=username).exclude(username='admin').exists():
            errors['username'] = "Username is already taken"
            return render(request, 'signup.html', {'errors': errors})

        # Check if the email already exists (except admin email)
        if CustomUser.objects.filter(email=email).exclude(email='admin@gmail.com').exists():
            errors["email"] = "Email is already taken"
            return render(request, 'signup.html', {'errors': errors})


        # Check if password and confirm password match
        if password != confirm_password:
            errors["confirm_password"] = "Passwords do not match!"

        # If there are errors, return the signup page with errors
        if errors:
            return render(request, 'signup.html', {'errors': errors})

        # # Create a new user if no errors
        # user = CustomUser.objects.create_user(email=email, username=username, password=password)
        # user.set_password(password)  # Hash the password
        # user.save()

        # # After user is created, redirect to the login page
        # messages.success(request, 'Account created successfully! You can now log in.')
        # return redirect('login')
        try:
            user = CustomUser.objects.create_user(email=email, username=username, password=password)
            user.set_password(password)  # Hash the password
            user.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')

        except Exception as e:
            errors["server"] = "An error occurred while creating the user: " + str(e)
            return render(request, 'signup.html', {'errors': errors})

    return render(request, 'signup.html')

def signinview(request):
    if request.method == 'POST':
        errors = {}
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=user_name, password=password)

        if user is None:
            errors["user"] = "User does not exist"
        
        if errors:
            return render(request, "signin.html", {'errors': errors})
        else:
            login(request, user)
            messages.success(request, 'Login successful')

            # Check if the user is an admin (staff)
            if user.is_staff:  # Admin user
                return redirect('addproduct')  # Admin goes to the add product page
            else:  # Regular customer
                return redirect('productlist')  # Customer goes to the product list page

    return render(request, 'signin.html')

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
@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user

    # Check if the product is already in the user's cart
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)

    if not created:
        # If item already exists, update the quantity
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'{product.productname} added to cart!')
    return redirect('productlist')
@login_required(login_url='login')
def view_cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    return render(request, 'addcart.html', {'cart_items': cart_items})