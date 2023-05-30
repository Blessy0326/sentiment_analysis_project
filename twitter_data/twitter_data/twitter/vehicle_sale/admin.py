from django.contrib import admin
from .models import Product,User,Review_added,Classification,Admin

# Register your models here.
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Review_added)
admin.site.register(Classification)
admin.site.register(Admin)


