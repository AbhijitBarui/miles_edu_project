from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import CustomLoginSerializer, UserRegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from actions.models import UserActivityLog
from accounts.models import User


class CustomLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CustomLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.user  # Comes from your serializer

        # Log login
        UserActivityLog.objects.create(
            user=user,
            action_type="Login",
            metadata={
                "ip": request.META.get("REMOTE_ADDR"),
                "user_agent": request.META.get("HTTP_USER_AGENT")
            },
            status="DONE"
        )

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class CustomLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Log logout
            UserActivityLog.objects.create(
                user=request.user,
                action_type="Logout",
                metadata={
                    "ip": request.META.get("REMOTE_ADDR"),
                    "user_agent": request.META.get("HTTP_USER_AGENT")
                },
                status="DONE"
            )

            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]  

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Log registration
            UserActivityLog.objects.create(
                user=user,
                action_type="Register",
                metadata={
                    "ip": request.META.get("REMOTE_ADDR"),
                    "user_agent": request.META.get("HTTP_USER_AGENT")
                },
                status="DONE"
            )

            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
