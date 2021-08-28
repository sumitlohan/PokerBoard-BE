from django.db import models

from apps.user.models import CustomBase, User


class Pokerboard(CustomBase):
    '''
    Pokerboard settings class
    '''
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
    manager = models.ForeignKey(User, on_delete=models.CASCADE, help_text='Owner of Pokerboard')
    title = models.CharField(unique=True, max_length=20, help_text='Name of Pokerboard')
    description = models.CharField(max_length=100, help_text='Description')
    estimation_type = models.CharField(choices=ESTIMATION_CHOICES, max_length=20, help_text='Estimation type', default="SERIES")
    duration = models.IntegerField(help_text='Duration for voting (in secs)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="STARTED")
    
    def __str__(self):
        return self.title


class Ticket(CustomBase):
    """
    Ticket details class
    """
    pokerboard = models.ForeignKey(Pokerboard, on_delete=models.CASCADE, help_text="Pokerboard to which ticket belongs")
    ticket_id = models.SlugField(help_text="Ticket ID imported from JIRA")
    estimate = models.IntegerField(help_text="Final estimate of ticket")
    rank = models.IntegerField(help_text="Rank of ticket")

    def __str__(self):
        return self.ticket_id
