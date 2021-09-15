import json
import requests

from rest_framework.serializers import ValidationError

from apps.pokerboard import constants as pokerboard_constants



class JiraApi:
    """
    Jira API Utilities
    """

    @staticmethod
    def query_jira(method, url, payload=None, status_code=200):
        """
        Perform a request and returns response
        """
        if not payload:
            payload = {}
        response = requests.request(method, url, headers=pokerboard_constants.JIRA_HEADERS, data=payload)
        if response.status_code != status_code:
            error_msgs = ["Something went wrong"]
            res = json.loads(response.text)
            error_msgs = res.get("errorMessages", error_msgs)
            raise ValidationError(error_msgs)
        if not response.text:
            return {}
        return json.loads(response.text)

    @staticmethod
    def get_sprints(boardId):
        """
        Get sprints for a given board
        """
        sprint_res = JiraApi.query_jira("GET", f"{pokerboard_constants.JIRA_API_URL_V1}board/{boardId}/sprint")
        return sprint_res["values"]

    @staticmethod
    def get_boards():
        """
        Get all available boards
        """
        boards_url = f"{pokerboard_constants.JIRA_API_URL_V1}board"
        boards_res = JiraApi.query_jira("GET", boards_url)
        return boards_res["values"]

    @staticmethod
    def get_all_sprints():
        """
        Fetches all sprints from all available boards
        """
        boards = JiraApi.get_boards()
        sprints = []
        for board in boards:
            sprints = sprints + JiraApi.get_sprints(board["id"])
        return sprints
