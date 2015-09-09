# import the User object
from dashboard.models import User
from django.contrib.auth.hashers import check_password
import json
# Name my backend 'MyCustomBackend'
class DashBoardBackend:

    # Create an authentication method
    # This is called by the standard Django login procedure
    def authenticate(self, email=None, password=None, password_token = None, social = False):
        try:
            if password_token:
                user = User.objects.get(password_token=password_token)
                return user
            elif email and password:
                # Try to find a user matching your username
                user = User.objects.get(email__iexact=email)
                #  Check the password is the reverse of the username
                if user and check_password(password, user.password):
                    # Yes? return the Django user object
                    return user
            elif email and social:
                user = User.objects.get(email__iexact=email)
                return user
            else:
                # No? return None - triggers default login failed
                return None
        except Exception as e:
            print e
            # No user was found, return None - triggers default login failed
            return None

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None