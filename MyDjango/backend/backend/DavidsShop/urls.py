from django.urls import path
from . import views

urlpatterns = [
   path('', views.index),
   path('addbasket/<int:ProductID>', views.add_to_basket, name="add_basket"),
   path('products/<int:ProductID>', views.product_individual, name="individual_product" )
]