from django.conf.urls.defaults import *


urlpatterns = patterns('',
)

# BOGUS Make conpac.puzzlers.org and convidence.puzzlers.org redirect to the subdirectory


# BOGUS KIWI INSTALL- can this autoinstall?
from kiwi import kiwitemplates
kiwitemplates.setupURLs(urlpatterns)