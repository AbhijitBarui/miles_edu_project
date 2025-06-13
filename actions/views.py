from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UserActivityLog
from .serializers import UserActivityLogSerializer

class UserActivityLogViewSet(viewsets.ModelViewSet):
    queryset = UserActivityLog.objects.all()
    serializer_class = UserActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return UserActivityLog.objects.all()

        queryset = UserActivityLog.objects.filter(user=user)

        action_type = self.request.query_params.get('action_type')
        search = self.request.query_params.get('search')
        start_date = self.request.query_params.get('start')
        end_date = self.request.query_params.get('end')

        if action_type:
            queryset = queryset.filter(action_type__iexact=action_type)

        if start_date and end_date:
            queryset = queryset.filter(timestamp__range=[start_date, end_date])

        return queryset


    def perform_create(self, serializer):
        request = self.request

        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')

        metadata = {
            "ip": ip_address,
            "user_agent": user_agent,
        }

        serializer.save(user=request.user, metadata=metadata)

    @action(detail=True, methods=['patch'])
    def transition(self, request, pk=None):
        activity = self.get_object()
        new_status = request.data.get('status')

        if new_status not in ['PENDING', 'IN_PROGRESS', 'DONE']:
            return Response({"error": "Invalid status"}, status=400)

        activity.status = new_status
        activity.save()
        return Response({"message": f"Status updated to {new_status}"})
