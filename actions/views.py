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
        queryset = UserActivityLog.objects.filter(user=user)

        action_type = self.request.query_params.get('action_type')
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')

        if action_type:
            queryset = queryset.filter(action_type=action_type)
        if start and end:
            queryset = queryset.filter(timestamp__range=[start, end])

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['patch'])
    def transition(self, request, pk=None):
        activity = self.get_object()
        new_status = request.data.get('status')

        if new_status not in ['PENDING', 'IN_PROGRESS', 'DONE']:
            return Response({"error": "Invalid status"}, status=400)

        activity.status = new_status
        activity.save()
        return Response({"message": f"Status updated to {new_status}"})
