"""
URL configuration for listaTareas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# agregue la carpeta task a las urls para poder llamar a la funcion helloworld cuando se visite el pad inicial
from task import views

#aqui se crean todas las rutas y se definen sus nombres y que funcion llamaran cuando se ejecuten
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # defino las llamdas desde la inicial
    path('signup/', views.signup, name='signup'),
    path('task/', views.task, name='task'),
    path('task_completed/', views.task_completed, name='task_completed'),
    path('logout/', views.cerrarSesion, name='cerrarSesion'),
    path('signin/', views.signin, name='signin'),
    path('task/create/', views.created_task, name='task_created'),
    path('task/<int:id>/', views.task_detail, name='task_detail'),
    path('task/<int:id>/complete/', views.complete_task, name='complete_task'),
    path('task/<int:id>/delated/', views.delated_task, name='delated_task'),
]
