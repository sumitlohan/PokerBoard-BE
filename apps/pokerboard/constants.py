from django.conf import settings


JIRA_HEADERS = {
    'Authorization': f'Basic {settings.JIRA_AUTH_TOKEN}',
    'Content-Type': 'application/json',
}

JIRA_API_URL_V1 = f"{settings.JIRA_URL}rest/agile/1.0/"
JIRA_API_URL_V2 = f"{settings.JIRA_URL}rest/api/2/"
GET_PROJECTS = f"{JIRA_API_URL_V2}jql/autocompletedata/suggestions?fieldName=project"
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
