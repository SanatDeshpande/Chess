"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings

from chess import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('game/<slug:user_id>', views.game, name='game'),
    path('game_state/<slug:user_id>', views.game_state, name='game_state'),
    path('init/', views.init, name='init'), #get init configuration
    path('action/<slug:user_id>/', views.action, name='request_action'),
    path('register_user/<slug:user_id>/', views.register_user, name='register_user'),
    path('join/<slug:game_id>/', views.join, name='join'),
]
