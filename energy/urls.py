from django.conf.urls import patterns, include, url

urlpatterns = patterns('energy.views',
    url(r'^$', 'index'),
    url(r'^result/$', 'result'),
)
