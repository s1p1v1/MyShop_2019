from django.conf.urls import url

import basket.views as basket

app_name = 'basket'

urlpatterns = [
    # url(r'^$', basket.BasketListView.as_view(), name='view'),
    url(r'^$', basket.basket, name='view'),
    # url(r'^add/(?P<pk>\d+)/$', basket.BasketAddView.as_view(), name='add'),
    url(r'^add/(?P<pk>\d+)/$', basket.basket_add, name='add'),
    # url(r'^remove/(?P<pk>\d+)/$', basket.BasketRemoveView.as_view(), name='remove'),
    url(r'^remove/(?P<pk>\d+)/$', basket.basket_remove, name='remove'),
    # url(r'^edit/(?P<pk>\d+)/(?P<quantity>\d+)/$', basket.BasketUpdateView.as_view(), name='edit'),
    url(r'^edit/(?P<pk>\d+)/(?P<quantity>\d+)/$', basket.basket_edit, name='edit'),
    url(r'^delete/(?P<pk>\d+)/$', basket.basket_delete, name='delete'),

]
