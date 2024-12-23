from django.core.validators import MinLengthValidator
from django.db import models


class Project(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In progress'),
        ('not_started', 'Not started'),
        ('completed', 'Completed'),
        ('looking_for_investor', 'Looking for investor'),
    ]

    name = models.CharField(
        max_length=50,
        validators=[
            MinLengthValidator(3),
        ],
    )

    description = models.TextField()

    business_plan = models.FileField(null=True, blank=True)

    media_files = models.FileField(null=True, blank=True)

    status = models.CharField(choices=STATUS_CHOICES)

    created_at = models.DateTimeField(auto_now=True)

    last_update = models.DateTimeField(auto_now_add=True)

    starting_at = models.DateField()

    finishing_at = models.DateField()

    start_up = models.ForeignKey(
        'profiles.StartUpProfile',
        on_delete=models.CASCADE,
    )

    investor = models.ForeignKey(
        'profiles.InvestorProfile',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
