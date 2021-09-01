import json
import requests

from rest_framework.serializers import ValidationError

import apps.pokerboard.constants as pokerboard_constants 

def query_jira(method, url, payload={}, status_code=200):
    """
    Permform a request and returns response
    """
    response = requests.request(method, url, headers=pokerboard_constants.JIRA_HEADERS, data=payload)
    if response.status_code != status_code:
        raise ValidationError("Something went wrong")
    res = json.loads(response.text)
    return res

