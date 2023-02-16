from django.urls import path
# import all from views
from . import views
# import format_suffix_patterns
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('products', views.product_list, name='products'),
    path('product/<int:pk>', views.single_product, name='product'),
    path('product/archive/<int:pk>', views.archive_or_activate_product, name='archive'),
    path('product/activate/<int:pk>', views.archive_or_activate_product, name='activate'),
    path('products/active', views.get_all_products, name='all_products'),
]

# do this if you want to obtain your results as json in the browser.
# just add .json to the end of the endpoint. Example /products.json
urlpatterns = format_suffix_patterns(urlpatterns)