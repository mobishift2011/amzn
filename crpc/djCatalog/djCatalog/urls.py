from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djBrand.views.home', name='home'),
    # url(r'^djBrand/', include('djBrand.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable tpthe admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^admin/', include('mongonaut.urls')),
)