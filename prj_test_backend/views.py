from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponse, Http404
from django.conf import settings
import os


def jwt_protected_media(request, path):
    auth = JWTAuthentication()
    try:
        # Try to authenticate the user using JWT
        user_auth_tuple = auth.authenticate(request)
        if user_auth_tuple is not None:
            # User is authenticated, serve the file
            file_path = os.path.join(settings.MEDIA_ROOT, path)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read())
                    response["Content-Type"] = 'image/jpeg' # Or the appropriate type
                    return response
            else:
                raise Http404("File not found")
        else:
            # Authentication failed
            return HttpResponse('Unauthorized', status=401)

    except:
        # Handle any other exceptions
        return HttpResponse('Unauthorized', status=401)