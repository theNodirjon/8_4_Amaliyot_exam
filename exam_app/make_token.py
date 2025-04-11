from datetime import datetime, timedelta

from rest_framework_simplejwt.tokens import RefreshToken

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh.set_exp(from_time=datetime.now(), life_time=timedelta(minutes=2))
    refresh.access_token.set_exp(from_time=datetime.now(), life_time=timedelta(minutes=2))

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }