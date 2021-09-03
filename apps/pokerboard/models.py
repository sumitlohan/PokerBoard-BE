from django.db import models

import apps.user.models as user_models


class Pokerboard(user_models.CustomBase):
    """
    Pokerboard settings class
    """
    ESTIMATION_CHOICES = (
        ("SERIES", "Series"),
        ("EVEN", "Even"),
        ("ODD", "Odd"),
        ("FIBONACCI", "Fibonacci"),
    )
    STATUS_CHOICES = (
        ("STARTED", "Started"),
        ("ENDED", "Ended")
    )
    manager = models.ForeignKey(user_models.User, on_delete=models.CASCADE, help_text='Owner of Pokerboard')
    title = models.CharField(unique=True, max_length=20, help_text='Name of Pokerboard')
    description = models.CharField(max_length=100, help_text='Description')
    estimation_type = models.CharField(choices=ESTIMATION_CHOICES, max_length=20, help_text='Estimation type', default="SERIES")
    duration = models.IntegerField(help_text='Duration for voting (in secs)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="STARTED")
    
    def __str__(self):
        return self.title


class Ticket(user_models.CustomBase):
    """
    Ticket details class
    """
    pokerboard = models.ForeignKey(Pokerboard, related_name="tickets", on_delete=models.CASCADE, help_text="Pokerboard to which ticket belongs")
    ticket_id = models.SlugField(help_text="Ticket ID imported from JIRA")
    estimate = models.IntegerField(null=True, help_text="Final estimate of ticket")
    rank = models.IntegerField(help_text="Rank of ticket")

    def __str__(self):
        return self.ticket_id


class GameSession(user_models.CustomBase):
    """
    GameSession model for storing each estimation session's details
    """
    IN_PROGRESS = "IN_PROGRESS"
    SKIPPED = "SKIPPED"
    ESTIMATED = "ESTIMATED"
    STATUS_CHOICES = (
        (IN_PROGRESS, "In progress"),
        (SKIPPED, "Skipped"),
        (ESTIMATED, "Estimated"),
    )
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="estimations")
    status = models.CharField(max_length=20, default="IN_PROGRESS", choices=STATUS_CHOICES)
    timer_started_at = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return f"{self.ticket.ticket_id} {self.status}"


class Vote(user_models.CustomBase):
    """
    Vote model for storing vote details for each user
    """
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="estimations")
    estimate = models.IntegerField()

    class Meta:
        unique_together = ('user', 'game_session')

    def __str__(self) -> str:
        return f"{self.user} {self.game_session.ticket.ticket_id} {self.estimate}"
