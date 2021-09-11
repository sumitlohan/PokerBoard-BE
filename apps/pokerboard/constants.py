from django.conf import settings


JIRA_HEADERS = {
    'Authorization': f'Basic {settings.JIRA_AUTH_TOKEN}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

MESSAGE_TYPES = ["estimate", "skip", "vote", "initialise_game", "start_timer"]

STORY_POINTS_FIELD = "customfield_10016"

FIBONACCI_OPTIONS = [1, 2, 3, 5, 8, 13, 21, 34]

JIRA_API_URL_V1 = f"{settings.JIRA_URL}rest/agile/1.0/"
JIRA_API_URL_V2 = f"{settings.JIRA_URL}rest/api/2/"
GET_PROJECTS = f"{JIRA_API_URL_V2}jql/autocompletedata/suggestions?fieldName=project"
