from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.contrib.auth.models import User
from recolectores.api.serializers import UserSerializer
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny

@extend_schema(
    request=UserSerializer,
    tags=["Autenticación"]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def Register(request):

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        
        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])

        user.save()

        return Response({"message": "Usuario creado correctamente"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Agregar el user_id al token
        token['user_id'] = user.id

        # Agregar los grupos del usuario al token
        token['groups'] = list(user.groups.values_list('name', flat=True))

        return token
    
# Sobrescribe el TokenObtainPairView
@extend_schema(tags=['Autenticación'])
@permission_classes([AllowAny])
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@extend_schema(tags=['Autenticación'])
@permission_classes([AllowAny])
class CustomTokenRefreshView(TokenRefreshView):
    pass