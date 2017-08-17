from django.http import QueryDict
        
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect


class HttpPostTunnelingMiddleware(object):
    def process_request(self, request):
        if request.META.has_key('HTTP_X_METHODOVERRIDE'):
            http_method = request.META['HTTP_X_METHODOVERRIDE']
            if http_method.lower() == 'put':
                request.method = 'PUT'
                request.META['REQUEST_METHOD'] = 'PUT'
                request.PUT = QueryDict(request.body)
            if http_method.lower() == 'delete':
                request.method = 'DELETE'
                request.META['REQUEST_METHOD'] = 'DELETE'
                request.DELETE = QueryDict(request.body)
        return None
    
class DisableCSRF(object):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

class AutoLogout:
    
    def process_request(self, request):
        try:
            last_activity =datetime.strptime(request.session['last_touch'], "%Y-%m-%d %H:%M:%S.%f")

            if datetime.now() - last_activity > timedelta( 0, settings.AUTO_LOGOUT_DELAY , 0):
                auth.logout(request)
#                 del request.session['last_touch']
                return HttpResponseRedirect("/")
        except KeyError:
            pass
    
        request.session['last_touch'] = str(datetime.now())