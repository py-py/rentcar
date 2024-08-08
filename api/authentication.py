import jwt
from core.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request


class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request: Request):
        header = request.headers.get("authorization")
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token

    def get_raw_token(self, header: bytes):
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if parts[0] != "Bearer":
            # Assume the header does not contain a JSON web token
            return None

        if len(parts) != 2:
            raise AuthenticationFailed(
                "Authorization header must contain two space-delimited values",
                code="bad_authorization_header",
            )

        return parts[1]

    def get_validated_token(self, raw_token: bytes):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        return jwt.decode(raw_token, options={"verify_signature": False})

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        user_id = validated_token["user_id"]
        user_email = validated_token["email"]

        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            user = User.objects.create_user(email=user_email, firebase_uid=user_id)

        if not user.is_active:
            raise AuthenticationFailed("User is inactive", code="user_inactive")

        return user
