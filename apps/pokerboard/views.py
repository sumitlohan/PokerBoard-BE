import json
from typing import Any
from typing_extensions import OrderedDict

from django.db.models.query import QuerySet

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.pokerboard import (
    constants as pokerboard_constants,
    models as pokerboard_models,
    serializers as pokerboard_serializers,
    utils as pokerboard_utils
)

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
        return pokerboard_models.Pokerboard.objects.filter(manager=self.request.user)\
                    .prefetch_related("tickets")


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
        url = f"{pokerboard_constants.JIRA_API_URL_V2}search?jql={jql}"

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
        sprints = pokerboard_utils.get_all_sprints()
        project_res = pokerboard_utils.query_jira("GET", pokerboard_constants.GET_PROJECTS)
        response = {
            "projects": project_res["results"],
            "sprints": sprints
        }
        return Response(response, status=status.HTTP_200_OK)


class CommentApiView(CreateAPIView, ListAPIView):
    """
    Comment on a Ticket on JIRA
    """
    serializer_class = pokerboard_serializers.CommentSerializer

    def get(self, request):
        """
        Get comments on a JIRA ticket
        """
        issueId = request.GET.get("issueId")
        response = pokerboard_utils.query_jira(method="GET", url=f"{pokerboard_constants.JIRA_API_URL_V2}issue/{issueId}/comment")
        return Response(response["comments"], status=status.HTTP_200_OK)

    def perform_create(self: CreateAPIView, serializer: Serializer) -> Any:
        """
        Comments on a JIRA ticket
        """
        issue = serializer.validated_data["issue"]
        comment = serializer.validated_data["comment"]
        url = f"{pokerboard_constants.JIRA_API_URL_V2}issue/{issue}/comment"
        payload = json.dumps({
            "body": comment
        })
        
        pokerboard_utils.query_jira("POST", url, payload=payload, status_code=201)


class TicketOrderApiView(APIView):
    """
    Ticket order API for ordering tickets
    """
    serializer_class = pokerboard_serializers.TicketOrderSerializer
    queryset = pokerboard_models.Ticket.objects.all()
    
    def put(self, request):
        """
        Changes ticket ordering
        """
        serializer = pokerboard_serializers.TicketOrderSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
