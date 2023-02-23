from django.urls import path

# import all from views
from . import views

# import format_suffix_patterns, login view and routers from rest_framework
from rest_framework.urlpatterns         import format_suffix_patterns
from rest_framework.authtoken.views     import obtain_auth_token
from rest_framework                     import routers

# do this if you want to have a default basic root view for DefaultRouter
router = routers.DefaultRouter()
urlpatterns = router.urls

urlpatterns += [
    path('products', views.product_list, name='products'),
    path('product/<int:pk>', views.single_product, name='product'),
    path('product/archive/<int:pk>', views.archive_or_activate_product, name='archive'),
    path('product/activate/<int:pk>', views.archive_or_activate_product, name='activate'),
    path('products/active', views.get_all_products, name='all_products'),
    path('register', views.register, name='register'),
    path('login', obtain_auth_token, name='login'),
    path('users', views.get_users, name='users'),
    path('users/<int:pk>', views.get_users, name='users')
]

# do this if you want to obtain your results as json in the browser.
# just add .json to the end of the endpoint. Example /products.json

# urlpatterns = format_suffix_patterns(urlpatterns)