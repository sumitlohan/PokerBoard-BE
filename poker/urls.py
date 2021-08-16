from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('account/', include('apps.user.urls')),
    path('groups/', include('apps.group.urls')),
]
