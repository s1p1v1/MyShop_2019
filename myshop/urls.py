"""myshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

import mainapp.views as mainapp

urlpatterns = [
    url(r'^$', mainapp.main, name='main'),
    url(r'^catalogue/', mainapp.catalogue, name='catalogue'),  # 16.09.19
    # url(r'^catalogue/', include('mainapp.urls', namespace='catalogue')),
    url(r'^contact/', mainapp.contact, name='contact'),
    url(r'^good/(\d+)/$', mainapp.good, name='good'),
    url(r'^auth/', include('authapp.urls', namespace='auth')),
    url(r'^basket/', include('basket.urls', namespace='basket')),
    url(r'^myadmin/', include('myadmin.urls', namespace='myadmin')),
    url(r'^search/$', mainapp.search, name='search'),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
