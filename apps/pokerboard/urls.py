from django.urls import path

from rest_framework.routers import SimpleRouter

import apps.pokerboard.views as pokerboard_views

router = SimpleRouter(trailing_slash=False)
router.register('',pokerboard_views.PokerboardApiView, basename="pokerboards")

urlpatterns = [
    path("jql", pokerboard_views.JqlAPIView.as_view()),
    path("comment", pokerboard_views.CommentApiView.as_view()),
    path("suggestions", pokerboard_views.SuggestionsAPIView.as_view()),
    path("game", pokerboard_views.GameSessionApi.as_view()),
    path("game/<int:pk>", pokerboard_views.GameSessionApi.as_view()),
    path("tickets/<int:pk>", pokerboard_views.TicketOrderApiView.as_view()),
] + router.urls
