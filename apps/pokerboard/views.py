import json
from typing import Any
from typing_extensions import OrderedDict

from django.conf import settings
from django.db.models.query import QuerySet

from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

import apps.pokerboard.constants as pokerboard_constants 
import apps.pokerboard.models as pokerboard_models
import apps.pokerboard.serializers as pokerboard_serializers
import apps.pokerboard.utils as pokerboard_utils 


class PokerboardApiView(ModelViewSet):
    """
    Pokerboard API for getting pokerboard list/details, and creating pokerboard.
    """

    http_method_names = ["get", "post"]
    
    def get_serializer_class(self: ModelViewSet) -> Serializer:
        """
        Get serializer class based on request's method
        """
        if self.request.method == "POST":
            return pokerboard_serializers.CreatePokerboardSerializer
        return pokerboard_serializers.PokerboardSerializer

    def get_queryset(self: ModelViewSet) -> QuerySet:
        """
        Get pokerboards a user can access
        """
        return pokerboard_models.Pokerboard.objects.filter(manager=self.request.user).prefetch_related("tickets")


class JqlAPIView(APIView):
    """
    Search By jql
    Get Issues for a project - project IN ("<project-name>")
    Get issues for a sprint - sprint IN ("sprint-name")
    Get issues from issues Id's list - issues IN ("KD-1", "KD-2")
    """
    def get(self: APIView, request: OrderedDict) -> Response:
        """
        Fetch JQL response given a JQL statement
        """
        jql = request.GET.get("jql")
        url = f"{settings.JIRA_URL}search?jql={jql}"

        res = pokerboard_utils.query_jira("GET", url)
        return Response(res, status=status.HTTP_200_OK)


class SuggestionsAPIView(APIView):
    """
    Get projects and sprints list from JIRA
    """
    def get(self: APIView, request: OrderedDict) -> Response:
        """
        Fetch available sprints and projects
        """
        sprint_res = pokerboard_utils.query_jira("GET", pokerboard_constants.GET_SPRINTS)
        project_res = pokerboard_utils.query_jira("GET", pokerboard_constants.GET_PROJECTS)
        response = {
            "projects": project_res["results"],
            "sprints": sprint_res["values"]
        }
        return Response(response, status=status.HTTP_200_OK)


class CommentApiView(CreateAPIView):
    """
    Comment on a Ticket on JIRA
    """
    serializer_class = pokerboard_serializers.CommentSerializer
    def perform_create(self: CreateAPIView, serializer: Serializer) -> Any:
        """
        Comments on a JIRA ticket
        """
        issue = serializer.validated_data["issue"]
        comment = serializer.validated_data["comment"]
        url = f"{settings.JIRA_URL}issue/{issue}/comment"
        payload = json.dumps({
            "body": comment
        })
        
        response = pokerboard_utils.query_jira("POST", url, payload=payload, status_code=201)


class TicketOrderApiView(UpdateAPIView):
    """
    Ticket order API for ordering tickets
    """
    serializer_class = pokerboard_serializers.TicketOrderSerializer
    queryset = pokerboard_models.Ticket.objects.all()


class GameSessionApi(CreateAPIView):
    """
    Game session API for creating game and fetching active game session
    """
    serializer_class = pokerboard_serializers.GameSessionSerializer
    queryset = pokerboard_models.GameSession.objects.all()
