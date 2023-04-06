from django.contrib.auth.tokens import PasswordResetTokenGenerator  
import six
from django.utils.http import int_to_base36
from django.utils.crypto import salted_hmac

class TokenGenerator(PasswordResetTokenGenerator):  
    def _make_hash_value(self, user, timestamp):  
        return (  
            six.text_type(user.pk) + six.text_type(timestamp) +  
            six.text_type(user.is_active)  
        )  

class PasswordResetToken(PasswordResetTokenGenerator): 
    def _make_hash_value(self, user, timestamp):  
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        return (  
            six.text_type(user.pk) + user.password +
            six.text_type(login_timestamp) + six.text_type(timestamp)
        )  

account_activation_token = TokenGenerator()  
password_reset_token = PasswordResetToken()