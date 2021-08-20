from rest_framework.routers import SimpleRouter

from apps.user import views


router = SimpleRouter(trailing_slash=False)
router.register(r'register', views.RegisterApi, basename='register')
urlpatterns = router.urls
