from django.core.validators import MinLengthValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class BaseProfile(models.Model):
    """
    Abstract base model for user profiles.

    Attributes:
        company_name (str): Unique name of the company.
        legal_name (str): Unique legal name of the company.
        email (str): Email address of the company (optional).
        phone_number (PhoneNumberField): Contact phone number (optional).
        region (str): Region where the company operates (optional).
        industry_type (str): Industry type of the company (optional).
        logo (ImageField): Logo of the company (optional).
        user (ForeignKey): User associated with the profile.
    """
    MIN_LENGTH_DEFAULT = 3
    MAX_LENGTH_DEFAULT = 50
    PHONE_NUMBER_MAX_LEN = 15

    company_name = models.CharField(
        unique=True,
        max_length=MAX_LENGTH_DEFAULT,
        validators=[MinLengthValidator(MIN_LENGTH_DEFAULT)],
    )

    legal_name = models.CharField(
        unique=True,
        max_length=MAX_LENGTH_DEFAULT,
        validators=[MinLengthValidator(MIN_LENGTH_DEFAULT)],
    )

    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
    )

    phone_number = PhoneNumberField(
        blank=True,
        null=True,
    )

    region = models.CharField(
        max_length=MAX_LENGTH_DEFAULT,
        validators=[MinLengthValidator(MIN_LENGTH_DEFAULT)],
        null=True,
        blank=True,
    )

    industry_type = models.CharField(
        max_length=MAX_LENGTH_DEFAULT,
        validators=[MinLengthValidator(MIN_LENGTH_DEFAULT)],
        null=True,
        blank=True,
    )

    logo = models.ImageField(null=True, blank=True)

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
    )

    def __str__(self):
        """
        Return a string representation of the profile.

        Returns:
            str: The company name of the profile.
        """
        return str(self.company_name)

    class Meta:
        abstract = True


class StartUpProfile(BaseProfile):
    """
    Model for startup profiles.

    Attributes:
        user (ForeignKey): User associated with the profile.
        project_information (TextField): Detailed information about the project.
        company_size (PositiveIntegerField): Size of the company (optional).
        investment_needs (DecimalField): Amount of investment needed (optional).
    """
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
    )
    project_information = models.TextField()
    company_size = models.PositiveIntegerField(null=True, blank=True)
    investment_needs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.user)


class InvestorProfile(BaseProfile):
    """
    Model for investor profiles.

    Inherits all attributes from BaseProfile.
    """
    pass