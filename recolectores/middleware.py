import jwt
from django.conf import settings
from django.shortcuts import redirect
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.session.get('jwt_token')

        if token:
            try:
                # Decodificar el token
                jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            except ExpiredSignatureError:
                # Token expirado, eliminarlo de la sesión
                del request.session['jwt_token']
                return redirect('login')

            except InvalidTokenError:
                # Token inválido, eliminarlo de la sesión
                del request.session['jwt_token']
                return redirect('login')

        response = self.get_response(request)
        return response