from django.urls import path
from . import views

urlpatterns = [

    path('', views.login, name='login'),
    path('signin/', views.signin, name="signin"),
    path('landing/index.html', views.index, name='index'),
    path('logout', views.logout, name='logout')
]
