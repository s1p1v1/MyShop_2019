from django.conf.urls import url

import mainapp.views as mainapp

# обязательно указывать для django 2.0
app_name = 'mainapp'

urlpatterns = [
    url(r'^$', mainapp.catalogue),  # 16.09.19
    # url(r'^(\d+)/$', mainapp.good, name='good'),
    # url(r'^country/(\d+)/$', mainapp.country, name='country'),
    # url(r'^country/(?P<count_pk>\d+)/page/(?P<page>\d+)/$', mainapp.catalogue, name='country_catalogue'),
    # url(r'^country/(?P<count_pk>\d+)/page/(?P<page>\d+)/$', mainapp.catalogue, name='country_catalogue'),
    # 16.09.19
    # url(r'^country/(?P<pk>\d+)/$', mainapp.catalogue, name='country'),
    # url(r'^country/(?P<pk>\d+)/page/(?P<page>\d+)/$', mainapp.catalogue, name='page'),
    # url(r'^page/(?P<page>\d+)/$', mainapp.catalogue, name='page'),
    # url(r'^rating/(\d+)/$', mainapp.product_rating_accounting, name='rating'),
]
