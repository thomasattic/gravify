from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^jdata/(?P<token>.*)$', "restapi.jdata"),
    (r'^newsession$', "restapi.newsession"),
    (r'^email/(?P<operator>.*)/(?P<email>.*)$', "emailsignup.handler"),
)


# BOGUS KIWI INSTALL- can this autoinstall?
from kiwi import kiwitemplates
kiwitemplates.setupURLs(urlpatterns)