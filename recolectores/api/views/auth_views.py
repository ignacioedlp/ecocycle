from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import User
from recolectores.api.serializers import UserSerializer
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

@extend_schema(
    request=UserSerializer,
    tags=["Autenticación"]
)
@api_view(['POST'])
def Register(request):

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        
        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])

        user.save()

        return Response({"message": "Usuario creado correctamente"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Autenticación'])
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema(tags=['Autenticación'])
class CustomTokenRefreshView(TokenRefreshView):
    pass