from django.urls import path

from rest_framework.routers import SimpleRouter

from apps.pokerboard.views import JqlAPIView, SuggestionsAPIView, PokerboardApiView, CommentApiView

router = SimpleRouter(trailing_slash=False)
router.register('',PokerboardApiView, basename="pokerboards")

urlpatterns = [
    path("jql", JqlAPIView.as_view()),
    path("comment", CommentApiView.as_view()),
    path("suggestions", SuggestionsAPIView.as_view()),

] + router.urls
