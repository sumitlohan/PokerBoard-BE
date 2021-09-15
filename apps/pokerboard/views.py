import json
from typing import Any
from typing_extensions import OrderedDict

from django.db.models.query import QuerySet

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet

from apps.pokerboard import (
    constants as pokerboard_constants,
    models as pokerboard_models,
    permissions as pokerboard_permissions,
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
        queryset = pokerboard_models.Pokerboard.objects.filter(manager=self.request.user)\
                    .prefetch_related("tickets")
        invites = pokerboard_models.Pokerboard.objects.filter(invite__invitee=self.request.user, invite__is_accepted=True)
        return (queryset.union(invites))


class JqlAPIView(RetrieveAPIView):
    """
    Search By jql
    Get Issues for a project - project IN ("<project-name>")
    Get issues for a sprint - sprint IN ("sprint-name")
    Get issues from issues Id's list - issues IN ("KD-1", "KD-2")
    """
    def get(self: RetrieveAPIView, request: OrderedDict) -> Response:
        """
        Fetch JQL response given a JQL statement
        """
        jql = request.GET.get("jql")
        url = f"{pokerboard_constants.JIRA_API_URL_V2}search?jql={jql}"

        res = pokerboard_utils.query_jira("GET", url)
        return Response(res, status=status.HTTP_200_OK)


class SuggestionsAPIView(RetrieveAPIView):
    """
    Get projects and sprints list from JIRA
    """
    def get(self: RetrieveAPIView, request: OrderedDict) -> Response:
        """
        Fetch available sprints and projects
        """
        sprints = pokerboard_utils.get_all_sprints()
        project_res = pokerboard_utils.query_jira("GET", pokerboard_constants.GET_PROJECTS_URL)
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

    def get(self: ListAPIView, request: OrderedDict) -> Response:
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


class TicketOrderApiView(UpdateAPIView):
    """
    Ticket order API for ordering tickets
    """
    serializer_class = pokerboard_serializers.TicketOrderSerializer
    queryset = pokerboard_models.Ticket.objects.all()

    def put(self: UpdateAPIView, request: OrderedDict, pk: int=None) -> Response:
        """
        Changes ticket ordering
        """
        serializer = pokerboard_serializers.TicketOrderSerializer(data=request.data, context={"pk": pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PokerboardMembersApi(ModelViewSet):
    serializer_class = pokerboard_serializers.InviteUserSerializer
    pokerboard_member_serializer = pokerboard_serializers.PokerboardMemberSerializer
    queryset = pokerboard_models.Invite.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [AllowAny]
        if self.action == 'create' or self.action == 'destroy': 
            permission_classes = [pokerboard_permissions.IsManagerPermission]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        Invites a user/group to pokerboard
        Only pokerboard's manager can perform this action
        """
        pokerboard = pokerboard_models.Pokerboard.objects.get(id=self.request.data['pokerboard'])
        self.check_object_permissions(self.request, pokerboard)
        return super().perform_create(serializer)

    def retrieve(self, request, pk = None):
        """
        Gets all the pokerboard's members
        """
        invitee = pokerboard_models.Invite.objects.filter(pokerboard=pk, is_accepted=True)
        members = self.pokerboard_member_serializer(invitee, many=True)
        return Response(members.data)

    def update(self, request, pk = None, *args, **kwargs):
        """
        Invitation acception API
        """
        instance = self.queryset.get(id=pk)
        if instance.invitee == self.request.user.email and instance.is_accepted == False:
            instance.is_accepted = True
            instance.save()
            return Response(status=HTTP_200_OK)

        return Response(status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk = None, *args, **kwargs):
        """
        Removes member from pokerboard
        Only pokerboard's manager can perform this action
        """
        instance = self.queryset.get(id=pk)
        pokerboard = pokerboard_models.Pokerboard.objects.get(id=instance.pokerboard.id)
        self.check_object_permissions(self.request, pokerboard)
        if instance:
            instance.delete()

            return Response(status=HTTP_200_OK)

        return Response(status=HTTP_400_BAD_REQUEST)
