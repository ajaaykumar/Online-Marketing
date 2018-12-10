"""online_Marketing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from online_Marketing import settings
from Product_App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.showindex, name='home'),
    path('category/', views.showcategory, name='category'),
    path('<str:category_slug>', views.showcategory, name='product_list_by_category'),
    path('signup/', views.Signup, name='signup'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('<int:product_id>/', views.DisplayDetails, name='display'),
    path('createnew/', views.createNewProduct, name='createnew'),
    path('create/', views.saveProduct, name='create'),
    path('profile/', views.profilepage, name='profile'),
    # path('results/', views.search, name='results'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#category--->1
#states--->1000
#citys---> 10000
