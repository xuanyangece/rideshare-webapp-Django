from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('display/<int:id>/', views.display, name='display'),
    path('display/<int:id>/<int:rid>/delete/', views.delete, name='delete'),
    path('display/<int:id>/<int:rid>/', views.curtride, name='curtride'),
    path('display/<int:id>/<int:rid>/complete/', views.complete, name='complete'),
    path('display/<int:id>/findride/driver/', views.findridedriver, name='findridedriver'),
    path('display/<int:id>/<int:rid>/handledrive', views.handledrive, name='handledrive'),
    path('user/<int:id>/', views.profile, name='profile'),
    path('user/<int:id>/regisdriver', views.regisdriver, name='regisdriver'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:id>/newride/', views.newride, name='newride'),
    path('<int:id>/newshare/', views.newshare, name='newshare'),
    path('<int:id>/<int:rid>/<int:passenger>/joinshare', views.joinshare, name='joinshare'),
    path('<int:id>/<int:rid>/deleteshare', views.deleteshare, name='deleteshare')
]
