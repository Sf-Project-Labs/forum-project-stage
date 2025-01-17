from django.core.management.base import BaseCommand
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError  # Correct import
from ...models import TokenRecord


class Command(BaseCommand):
    help = "Remove expired tokens from the TokenRecord table."

    def handle(self, *args, **kwargs):
        expired_count = 0

        for token_record in TokenRecord.objects.all():
            try:
                # Validate Access Token
                AccessToken(token_record.access_token)
            except TokenError:
                token_record.delete()
                expired_count += 1
                continue  # Skip validating the Refresh Token

            try:
                # Validate Refresh Token
                RefreshToken(token_record.refresh_token)
            except TokenError:
                token_record.delete()
                expired_count += 1

        self.stdout.write(f"Deleted {expired_count} expired tokens.")
