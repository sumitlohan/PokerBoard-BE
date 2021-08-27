import json
import requests

from django.conf import settings

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.pokerboard.models import Pokerboard
from apps.pokerboard.serializers import PokerboardSerializer, CommentSerializer


class PokerboardApiView(ModelViewSet):
    """
    pokerboard API
    """
    
    serializer_class = PokerboardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Pokerboard.objects.filter(manager=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(manager=self.request.user)


headers = {
'Authorization': f'Basic {settings.JIRA_AUTH_TOKEN}',
'Content-Type': 'application/json',
}


class JqlAPIView(APIView):
    """
    Search By jql
    Get Issues for a project - project IN ("<project-name>")
    Get issues for a sprint - sprint IN ("sprint-name")
    Get issues from issues Id's list - issues IN ("KD-1", "KD-2")
    """
    def get(self, request):
        jql = request.data.get("jql")
        url = f"{settings.JIRA_URL}search?jql={jql}"

        response = requests.request("GET", url, headers=headers)
        if response.status_code!=200:
            raise ValidationError("Something went wrong")
        res = json.loads(response.text)
        return Response(res, status=status.HTTP_200_OK)



class SuggestionsAPIView(APIView):
    """
    Get projects and sprints list from JIRA
    """
    def get(self, request):
        sprint_url = f"https://kaam-dhandha.atlassian.net/rest/agile/1.0/board/1/sprint"
        project_url = f"{settings.JIRA_URL}jql/autocompletedata/suggestions?fieldName=project"
        sprint_response = requests.request("GET", sprint_url, headers=headers)
        project_response = requests.request("GET", project_url, headers=headers)
        if sprint_response.status_code!=200 or project_response.status_code!=200:
            raise ValidationError("Something went wrong")
        sprint_res = json.loads(sprint_response.text)
        project_res = json.loads(project_response.text)
        response = {
            "projects": project_res["results"],
            "sprints": sprint_res["values"]
        }
        return Response(response, status=status.HTTP_200_OK)


class CommentApiView(CreateAPIView):
    """
    Comment on a Ticket
    """
    serializer_class = CommentSerializer
    def perform_create(self, serializer):
        issue = serializer.validated_data["issue"]
        comment = serializer.validated_data["comment"]
        url = f"{settings.JIRA_URL}issue/{issue}/comment"
        print(url)
        payload = json.dumps({
            "body": comment
        })
        
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response)
        if response.status_code!=201:
            raise ValidationError("Something went wrong")



"""
TODO:

Given ticket Id's, Create ticket objects
"""