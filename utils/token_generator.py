from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime, timedelta

class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"

    def check_token(self, user, token):
        # Token geçerlilik süresi 24 saat
        token_lifetime = 60 * 60 * 24
        return super().check_token(user, token) and (
            datetime.now() - datetime.fromtimestamp(user.last_login.timestamp())
        ).total_seconds() <= token_lifetime

token_generator = CustomPasswordResetTokenGenerator()
