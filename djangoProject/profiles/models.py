from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class BaseProfile(models.Model):
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


class StartUpProfile(BaseProfile):
    project_information = models.TextField()


class InvestorProfile(BaseProfile):
    pass
