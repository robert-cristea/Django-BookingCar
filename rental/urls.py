from django.urls import path

from rental import views

app_name = 'rental'

urlpatterns = [
    path('', views.index, name="index"),
    # path('loginVerify/', views.loginVerify, name='loginVerify'),
    path('viewCar/', views.viewCar, name='viewCar'),
    path('bookCar/', views.bookCar, name='book-car'),
    #path('<int:pk>/', views.ViewCar.as_view(), name='viewCar'),
]