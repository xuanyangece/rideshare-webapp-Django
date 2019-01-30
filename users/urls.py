from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('display/<int:id>/', views.display, name='display'),
    path('display/<int:id>/<int:rid>/', views.curtride, name='curtride'),
    path('user/<int:id>/', views.profile, name='profile'),
    path('user/<int:id>/regisdriver', views.regisdriver, name='regisdriver'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:id>/newride/', views.newride, name='newride')
]
