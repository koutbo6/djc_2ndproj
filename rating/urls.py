from django.conf.urls import patterns, url

urlpatterns = patterns('rating.views',
    # the main functionality
    url(r'^products/', 'product_list', name='product_list',),
    url(r'^createproduct/', 'create_product', name='create_product',),
    url(r'^product/(?P<pid>\d+)/$', 'product_details', name='product_details',),
    url(r'^rateproduct/(?P<pid>\d+)/$', 'product_rate', name='product_rate',),

    # the advanced functionality that you need to read on
    url(r'^productsentry/', 'product_list_entry', name='product_list_entry',),
    url(r'^aproducts/', 'advanced_product_list', name='advanced_product_list',),
)
