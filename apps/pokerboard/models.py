from django.db import models

import apps.user.models as user_models


class Pokerboard(user_models.CustomBase):
    """
    Pokerboard settings class
    """
    SERIES = 1
    EVEN = 2
    ODD = 3
    FIBONACCI = 4
    ESTIMATION_CHOICES = (
        (SERIES, "Series"),
        (EVEN, "Even"),
        (ODD, "Odd"),
        (FIBONACCI, "Fibonacci"),
    )

    STARTED = 1
    ENDED = 2
    STATUS_CHOICES = (
        (STARTED, "Started"),
        (ENDED, "Ended")
    )
    manager = models.ForeignKey(user_models.User, on_delete=models.CASCADE, help_text='Owner of Pokerboard')
    title = models.CharField(unique=True, max_length=20, help_text='Name of Pokerboard')
    description = models.CharField(max_length=100, help_text='Description')
    estimation_type = models.IntegerField(choices=ESTIMATION_CHOICES, help_text='Estimation type', default=SERIES)
    duration = models.IntegerField(help_text='Duration for voting (in secs)')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=STARTED)
    
    def __str__(self) -> str:
        return self.title


class Ticket(user_models.CustomBase):
    """
    Ticket details class
    """
    pokerboard = models.ForeignKey(Pokerboard, related_name="tickets", on_delete=models.CASCADE, help_text="Pokerboard to which ticket belongs")
    ticket_id = models.SlugField(help_text="Ticket ID imported from JIRA")
    estimate = models.IntegerField(null=True, help_text="Final estimate of ticket")
    rank = models.PositiveSmallIntegerField(help_text="Rank of ticket")

    class Meta:
        unique_together = ('pokerboard', 'rank')

    def __str__(self) -> str:
        return f'{self.ticket_id} - {self.pokerboard}'
