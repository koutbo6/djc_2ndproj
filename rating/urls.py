from django.conf.urls import patterns, url

urlpatterns = patterns('rating.views',
    url(r'^products/', 'product_list', name='product_list',),
    url(r'^productsentry/', 'product_list_entry', name='product_list_entry',),
    url(r'^createproduct/', 'create_product', name='create_product',),
    url(r'^product/(?P<pid>\d+)/$', 'product_details', name='product_details',),
    url(r'^rateproduct/(?P<pid>\d+)/$', 'product_rate', name='product_rate',),
)
