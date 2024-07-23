from rest_framework.authentication import BaseAuthentication


class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        raise NotImplementedError
