from . import views
from django.urls import path
from django.conf import  settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('',views.login_user, name = 'login'),
    path('home',views.home,name="home"),
    path('Product',views.all_product,name="product-list"),
    path('show_product/<product_id>',views.show_product,name="show-product"),
    path('rate',views.rate,name="rate"),
    path('rate_csv', views.review_csv, name='rate-csv'),
    path('classify',views.classification,name = 'classify'),
    path('tweets', views.classifytweets, name='tweets'),

    path('logout_user', views.logout_user, name="logout"),
    path('register_user', views.register_user, name="register-user"),
    path('naive', views.naivebayes, name="naive"),
    path('admin-login', views.login_user, name='admin-login'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)