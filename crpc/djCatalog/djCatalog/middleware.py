from django.http import HttpResponse
import base64

class BasicHTTPAuthenticationMiddleware(object):
    def process_request(self, request):
        if request.META.get('HTTP_AUTHORIZATION'):
            authtype, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
            if authtype == 'Basic':
                auth = base64.b64decode(auth)
                username, password = auth.split(':')
                if username == 'favbuy' and password == 'tempfavbuy':
                    return

        r = HttpResponse("Auth Required", status = 401)
        r['WWW-Authenticate'] = 'Basic realm="bat"'
        return r
