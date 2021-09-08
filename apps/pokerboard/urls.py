from django.urls import path

from rest_framework.routers import SimpleRouter

from apps.pokerboard import views as pokerboard_views

router = SimpleRouter(trailing_slash=False)
router.register('',pokerboard_views.PokerboardApiView, basename="pokerboards")

urlpatterns = [
    path("jql", pokerboard_views.JqlAPIView.as_view(), name="jql"),
    path("comment", pokerboard_views.CommentApiView.as_view(), name="comment"),
    path("suggestions", pokerboard_views.SuggestionsAPIView.as_view(), name="suggestions"),
    path("tickets", pokerboard_views.TicketOrderApiView.as_view(), name="tickets"),
] + router.urls
