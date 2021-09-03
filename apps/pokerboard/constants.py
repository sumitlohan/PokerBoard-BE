from django.conf import settings

JIRA_HEADERS = {
    'Authorization': f'Basic {settings.JIRA_AUTH_TOKEN}',
    'Content-Type': 'application/json',
}
GET_SPRINTS = "https://kaam-dhandha.atlassian.net/rest/agile/1.0/board/1/sprint"
GET_PROJECTS = f"{settings.JIRA_URL}jql/autocompletedata/suggestions?fieldName=project"

MESSAGE_TYPES = ["estimate", "skip", "vote", "initialise_game"]
