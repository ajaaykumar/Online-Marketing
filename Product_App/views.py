from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from .models import State
from .models import City
from .models import Category
from .models import Product
# Create your views here.

def showindex(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(status='published')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    return render(request, 'Product_App/index.html', {'category': category,
                                         'categories': categories,
                                         'products': products})

def Signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['cpassword']:
            try:
                User.objects.get(username=request.POST['Email'])
                return render(request, 'Product_App/signup.html', {'error': 'User Already Exist'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'], email=request.POST['Email'],
                                                password=request.POST['cpassword'])
                auth.login(request, user)
                return redirect('home')
        else:
            return render(request, 'Product_App/signup.html', {'error': 'Password does not match'})
    else:
        return render(request, 'Product_App/signup.html')


def Login(request):
    if request.method == 'POST':
        # if user wants to login # authenticate will check if user is available or not
        user = auth.authenticate(username=request.POST['Email'], password=request.POST['password'])
        # if user available
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        # if user does not exist
        else:
            return render(request, 'Product_App/login.html', {'error': 'username and password is does not match'})
    else:
        return render(request, 'Product_App/login.html')


def Logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')

@login_required(login_url='/signup/')
def AddProduct(request):
    states = State.objects.all()
    citys = City.objects.all()
    products = Product.objects.all()
    if request.method == 'POST':
            product = Product()
            product.title = request.POST['title']
            product.category = request.POST['category']
            product.phone_no = request.POST['Phone No']
            product.city = request.POST['City']
            product.state = request.POST['State']
            product.location = request.POST['location']
            product.description = request.POST['description']
            product.pub_date = timezone.datetime.now()
            product.image = request.FILES['image']
            product.hunter = request.user
            product.save()
            print('-------------->', product.id)
            return redirect('create/' + str(product.id))
    else:
        return render(request, 'Product_App/addproduct.html', {'states': states, 'citys': citys, 'products': products})

@login_required(login_url='/login/')
def DisplayDetails(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'Product_App/display.html', {'product': product})


# def search(request):
# #     query = request.GET.get('q')
# #     if query:
# #         results = Product.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
# #     else:
# #         results = Product.objects.filter(status='published')
# #     return render(request, 'Product_App/index.html', {'query': query})

def search(request):
    if request.method == 'POST':
        srch = request.POST['q']

        if srch:
            match = Product.objects.filter(Q(title__icontains=srch) | Q(body__icontains=srch))

            if match:
                return render(request, 'Product_App/index.html', {'sr': match})
            else:
                messages.error(request, 'No result found')
        else:
            return HttpResponseRedirect('/search/')




