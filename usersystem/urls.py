from django.urls import path, include

from . import views

app_name = 'usersystem'
urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
    path('register/', views.register, name='register')
]
