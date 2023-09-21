"""
URL configuration for uemarketplace project.

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

from core.views import frontpage
from core.views import htmx_rocks
from core.views import pixel_streaming
from core.views import generate_ssh_key


urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('admin/', admin.site.urls),
    path('templates/core/partials/htmx_rocks.html', htmx_rocks, name='htmx_rocks'),
    path('templates/core/partials/pixel_streaming.html', pixel_streaming, name='pixel_streaming'),
    path('generate_key/', generate_ssh_key, name='generate_ssh_key'), 
]
