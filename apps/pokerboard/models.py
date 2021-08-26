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
