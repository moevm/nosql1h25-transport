from django.urls import path
from . import views

urlpatterns = [
    path("", views.bd_watching,name= 'bd_watching'),
    path("create_order", views.create_order,name= 'create_order'),
    path("catalog", views.catalog,name= 'catalog'),
    path("profile", views.profile,name= 'profile')
] 
