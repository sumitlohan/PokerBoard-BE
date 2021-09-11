import json
import requests

from rest_framework.serializers import ValidationError

import apps.pokerboard.constants as pokerboard_constants 

def query_jira(method, url, payload="{}", status_code=200):
    """
    Permform a request and returns response
    """
    response = requests.request(method, url, headers=pokerboard_constants.JIRA_HEADERS, data=payload)
    print("start")
    print(response)
    print("End")
    if response.status_code != status_code:
        raise ValidationError("Something went wrong")
    result = response.text if response.text else "{}"
    return json.loads(result)

def validate_vote(deck_type, estimate):
    print(deck_type)
    print(estimate)
    if deck_type == "EVEN":
        if estimate % 2 == 1:
            raise ValidationError("Invalid estimate")
    elif deck_type == "ODD":
        if estimate % 2 == 0:
            raise ValidationError("Invalid estimate")
    elif deck_type == "FIBONACCI":
        if estimate not in pokerboard_constants.FIBONACCI_OPTIONS:
            raise ValidationError("Invalid estimate")


def get_all_sprints():
    boards_url = f"{pokerboard_constants.JIRA_API_URL_V1}board"
    boards_res = query_jira("GET", boards_url)
    sprints = []
    for board in boards_res["values"]:
        sprint_res = query_jira("GET", f"{pokerboard_constants.JIRA_API_URL_V1}board/{board['id']}/sprint")
        sprints = sprints + sprint_res["values"]
    return sprints