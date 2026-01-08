from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status


class LoginApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )
        
        # check user credentials
        if not user:
            return Response(
                {'error': 'invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # get token if it exists or create new one
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key
        }, status=status.HTTP_200_OK)


# logout and delete token
class LogoutApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response({
            'message': 'logged out successfully'
        })
