from sqlite3 import IntegrityError

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from .models import State
from .models import City
from .models import Category
from .models import Product

# Create your views here.
def showindex(request):
    state = State.objects.all()
    city = City.objects.all()
    category = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'Product_App/index.html', {'state': state, 'city': city,
                                                     'category': category, 'products': products})

def showcategory(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    # products = Product.objects.filter(status='published')
    products = Product.objects.all()
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
                User.objects.get(username=request.POST['username'])
                return render(request, 'Product_App/signup.html', {'error': 'User Already Exist'})
            except IntegrityError:
                return render(request, 'Product_App/signup.html', {'error': 'User Already Exist'})

            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'],
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

@login_required(login_url='/login/')
def DisplayDetails(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'Product_App/display.html', {'product': product})


def createNewProduct(request):
    # categoury dropdown box
    cate = Category.objects.values('name')
    categorys = ['Category']
    for val in cate:
        categorys.append(val['name'])

        # state dropdown
    stname = State.objects.values('name')
    states = ['State']
    for valu in stname:
        states.append(valu['name'])
    # get city from state

    sel_state = request.GET.get("state")
    # getting state id no
    res = State.objects.values('idno').filter(name=sel_state)
    idno = 0
    for x in res:
        idno = x["idno"]
    # finding city from state id no
    res1 = City.objects.values('city_name').filter(state_name=idno)
    citys = ["City"]
    if not res1:
        citys = ["No City Available"]
    else:
        for x in res1:
            citys.append(x['city_name'])

    # cname = City.objects.values('city_name')
    # citys = ['City']
    # for val in cname:
    #     citys.append(val['city_name'])
    return render(request, 'Product_App/addproduct.html', {'categorys': categorys, 'states': states, 'citys': citys, "key":"one"})


def saveProduct(request):
    if request.method == 'POST':
            title = request.POST.get('title')
            category = request.POST.get('category')
            description = request.POST.get('description')
            # image = request.POST.get('image')
            price = request.POST.get('price')
            name = request.POST.get('name')
            phone_no = request.POST.get('phone_no')
            state = request.POST.get('state')
            city = request.POST.get('city')
            location = request.POST.get('location')
            print('>>>>>>>>>>>', title, category, description, name, phone_no, price, city, state, location)

            res = Category.objects.values('idno').filter(name=category)
            idno = 0
            for x in res:
                idno = x['idno']

            sta = State.objects.values('idno').filter(name=state)
            sidno = 0
            for y in sta:
                sidno = y['idno']

            cit = City.objects.values('idno').filter(city_name=city)
            cidno = 0
            for z in cit:
                cidno = z['idno']

            product = Product(title=title, body=description, price=price, name=name,phoneno=phone_no, plocation=location,
                              category=Category.objects.get(idno=idno),
                              state=State.objects.get(idno=sidno),
                              city=City.objects.get(idno=cidno),)
            product.image = request.FILES['image']
            product.hunter = request.user
            product.save()
            # return redirect('create/' + str(product.id))
            return render(request, 'Product_App/index.html/')
    else:
        return render(request, 'Product_App/addproduct.html',)

@login_required(login_url='/login/')
def profilepage(request):
    user = User.objects.all()
    return render(request, 'Product_App/Profile.html', {'user': user})
