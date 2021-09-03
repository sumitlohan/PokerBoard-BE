from django.db import models

from apps.user.models import CustomBase, User


class Pokerboard(CustomBase):
    """
    Pokerboard settings class
    """
    ESTIMATION_CHOICES = (
        (1, "Series"),
        (2, "Even"),
        (3, "Odd"),
        (4, "Fibonacci"),
    )
    STATUS_CHOICES = (
        (1, "Started"),
        (2, "Ended")
    )
    manager = models.ForeignKey(User, on_delete=models.CASCADE, help_text='Owner of Pokerboard')
    title = models.CharField(unique=True, max_length=20, help_text='Name of Pokerboard')
    description = models.CharField(max_length=100, help_text='Description')
    estimation_type = models.IntegerField(choices=ESTIMATION_CHOICES, help_text='Estimation type', default=1)
    duration = models.IntegerField(help_text='Duration for voting (in secs)')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    
    def __str__(self) -> str:
        return self.title


class Ticket(CustomBase):
    """
    Ticket details class
    """
    pokerboard = models.ForeignKey(Pokerboard, related_name="tickets", on_delete=models.CASCADE, help_text="Pokerboard to which ticket belongs")
    ticket_id = models.SlugField(help_text="Ticket ID imported from JIRA")
    estimate = models.IntegerField(null=True, help_text="Final estimate of ticket")
    rank = models.PositiveSmallIntegerField(help_text="Rank of ticket")

    def __str__(self) -> str:
        return f'{self.ticket_id} - {self.pokerboard}'
