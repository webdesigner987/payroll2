from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Use the user's primary key and the user's last_login field to generate the hash value
        return str(user.pk) + str(user.email) + str(timestamp)


account_activation_token = AccountActivationTokenGenerator()
