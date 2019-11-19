from django.conf.urls import url

import myadmin.views as myadmin

app_name = 'myadmin'

urlpatterns = [
    url(r'^users/create/$', myadmin.UserCreateView.as_view(), name='user_create'),
    url(r'^users/read/$', myadmin.UsersListView.as_view(), name='users'),
    url(r'^users/update/(?P<pk>\d+)/$', myadmin.UserUpdateView.as_view(), name='user_update'),
    url(r'^users/delete/(?P<pk>\d+)/$', myadmin.UserDeleteView.as_view(), name='user_delete'),

    # url(r'^countrys/$', myadmin.countrys, name='countrys'),
    url(r'^countrys/create/$', myadmin.CountryCreateView.as_view(), name='country_create'),
    url(r'^countrys/read/$', myadmin.CountrysListView.as_view(), name='countrys'),
    # url(r'^countrys/update/(?P<pk>\d+)/$', myadmin.CountryUpdateView.as_view(), name='country_update'),
    url(r'^countrys/update/(?P<pk>\d+)/$', myadmin.CountryCreateView.as_view(), name='country_update'),
    url(r'^countrys/delete/(?P<pk>\d+)/$', myadmin.CountryDeleteView.as_view(), name='country_delete'),

    # url(r'^products/create/country/(?P<pk>\d+)/$', myadmin.product_create, name='product_create'),
    url(r'^products/create/country/(?P<pk>\d+)/$', myadmin.ProductCreateView.as_view(), name='product_create'),
    # url(r'^products/read/country/(?P<pk>\d+)/$', myadmin.products, name='products'),
    url(r'^products/read/country/(?P<pk>\d+)/$', myadmin.CountryProductsView.as_view(), name='products'),
    url(r'^products/read/(?P<pk>\d+)/$', myadmin.ProductDetailView.as_view(), name='product_read'),
    url(r'^products/update/(?P<pk>\d+)/$', myadmin.ProductUpdateView.as_view(), name='product_update'),
    url(r'^products/delete/(?P<pk>\d+)/$', myadmin.ProductDeleteView.as_view(), name='product_delete'),
]
