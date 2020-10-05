import jwt
from django.conf import settings
from rest_framework import authentication
from users.models import User

# from rest_framework import exceptions


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.META.get("HTTP_AUTHORIZATION")
            # token 없을 경우 반드시 return None
            if token is None:
                return None
            xjwt, jwt_token = token.split("")
            decoded = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
            pk = decoded.get("pk")
            user = User.objects.get(pk=pk)
            return (user, None)
        except (ValueError, jwt.exceptions.DecodeError, User.DoesNotExist):
            return None
        # except jwt.exceptions.DecodeError:
        #     raise exceptions.AuthenticationFailed(detail="JWT Format Invalid")


""" 
AWS Elastic Beanstalk 등을 통해 배포하는 경우 
WSGIPassAuthorization On
조건 .conf 파일에 추가해야 함
"""