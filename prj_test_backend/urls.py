
from django.contrib import admin
from django.urls import re_path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from api.views import RegisterView, MyTokenObtainPairView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from prj_test_backend.views import jwt_protected_media

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # Jwt token endpoints
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # To set privilege on the media url
    # re_path(r'^media/(?P<path>.*)$', jwt_protected_media, name='jwt_protected_media'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)