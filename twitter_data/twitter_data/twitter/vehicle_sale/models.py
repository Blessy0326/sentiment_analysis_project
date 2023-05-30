from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Product(models.Model):

    product_name = models.CharField('Product Name',max_length = 30)
    web = models.URLField('Website Address')
    description = models.TextField(blank=True)
    product_image = models.ImageField(null=True,blank=True,upload_to="images/")

    def __str__(self):
        return self.product_name
class User(models.Model):

    name = models.CharField('User Name',max_length= 30)
    email_address = models.EmailField('Email')
    password = models.CharField('Password', max_length=30)
    phone = models.CharField('phone', max_length=10)
    def __str__(self):
        return self.name


class Classification(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True,on_delete=models.CASCADE)
    rate = models.CharField('Review',max_length = 30)


class Review_added(models.Model):
    product_selected = models.CharField('name', max_length=30)
    review =models.CharField('Review',max_length = 30)
    def __str__(self):
        return str(self.product_selected)

class Admin(models.Model):
    name = models.CharField('Admin Name',max_length= 30)
    password = models.CharField('Password', max_length=30)
    def __str__(self):
        return str(self.name)