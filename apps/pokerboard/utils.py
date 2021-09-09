import json
import requests

from rest_framework.serializers import ValidationError

from apps.pokerboard import constants as pokerboard_constants


def query_jira(method, url, payload={}, status_code=200):
    """
    Perform a request and returns response
    """
    response = requests.request(method, url, headers=pokerboard_constants.JIRA_HEADERS, data=payload)
    if response.status_code != status_code:
        error_msgs = ["Something went wrong"]
        try:
            res = json.loads(response.text)
            error_msgs = res["errorMessages"]
        except Exception:
            pass
        raise ValidationError(error_msgs)
    return json.loads(response.text)


def get_all_sprints():
    """
    Fetches all sprints from all available boards
    """
    boards_url = f"{pokerboard_constants.JIRA_API_URL_V1}board"
    boards_res = query_jira("GET", boards_url)
    sprints = []
    for board in boards_res["values"]:
        sprint_res = query_jira("GET", f"{pokerboard_constants.JIRA_API_URL_V1}board/{board['id']}/sprint")
        sprints = sprints + sprint_res["values"]
    return sprints
