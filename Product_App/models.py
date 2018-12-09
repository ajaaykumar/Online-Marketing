from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class State(models.Model):
    idno = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class City(models.Model):
    idno = models.IntegerField(primary_key=True)
    state_name = models.ForeignKey(State, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=50)

    def __str__(self):
        return self.city_name

class Category(models.Model):
    idno = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])

class Product(models.Model):
    STATUS_CHOICES = (
        ('published', 'published'),
        ('Draft', 'Draft'))
    title = models.CharField(max_length=50, default='')
    location = models.CharField(max_length=200, default='')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    hunter = models.ForeignKey(User, default="", on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='images/', blank=True)
    body = models.TextField(blank=True)
    plocation = models.CharField(max_length=100, default='')
    phoneno =models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, default='Draft', choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def pub_date_pretty(self):
        return self.created.strftime('%b %e %Y')

    def summary(self):
        return self.body[:100]

