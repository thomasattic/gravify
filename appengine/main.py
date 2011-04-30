# Initial main.py for a Kiwi project - this file is not copyrighted.
# You may modify this file as necessary

# Setup Django before anything else
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from google.appengine.dist import use_library
use_library('django', '1.2')

# General imports
import logging

# Google App Engine imports
from google.appengine.ext.webapp import util

# Force Django to reload its settings.
from django.conf import settings
settings._target = None

import django.core.handlers.wsgi
#import django.core.signals
#import django.db
#import django.dispatch.dispatcher

# Exception handler for Django problems
def log_exception(*args, **kwds):
    logging.exception('Exception in request:')

# Log errors.
#django.dispatch.dispatcher.connect(log_exception, django.core.signals.got_request_exception)

# Unregister the rollback event handler.
#django.dispatch.dispatcher.disconnect(django.db._rollback_on_exception, django.core.signals.got_request_exception)

# Register custom Django filters so they're available to all templates
# KIWI BOGUS: - can this be in kiwifilters itself?
from google.appengine.ext.webapp import template
template.register_template_library('kiwi.filters')

# The following setup of main facilitates profiling of the application by changing
# the single assignment statement at the bottom

def real_main():
    # Create a Django application for WSGI.
    application = django.core.handlers.wsgi.WSGIHandler()

    # Run the WSGI CGI handler with that application.
    util.run_wsgi_app(application)
    
def profile_main():
    # This is the main function for profiling 
    # We've renamed our original main() above to real_main()
    import cProfile, pstats, StringIO
    prof = cProfile.Profile()
    prof = prof.runctx("real_main()", globals(), locals())
    stream = StringIO.StringIO()
    stats = pstats.Stats(prof, stream=stream)
    stats.sort_stats("cumulative")  # time or cumulative
    stats.print_stats(80)  # lines to print
    # The rest is optional.
    # stats.print_callees()
    # stats.print_callers()
    logging.info("Profile data:\n%s", stream.getvalue())
 
main = real_main


if __name__ == '__main__':
    main()
