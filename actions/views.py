from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UserActivityLog
from .serializers import UserActivityLogSerializer
from rest_framework.permissions import IsAdminUser
from django.core.cache import cache


class UserActivityLogViewSet(viewsets.ModelViewSet):
    queryset = UserActivityLog.objects.all()
    serializer_class = UserActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        action_type = self.request.query_params.get('action_type')
        start_date = self.request.query_params.get('start')
        end_date = self.request.query_params.get('end')

        cache_key = f"user_logs:{user.id}:{action_type or ''}:{start_date or ''}:{end_date or ''}"
        cached_ids = cache.get(cache_key)

        if cached_ids:
            print("Fetching from Cache...") 
            return UserActivityLog.objects.filter(id__in=cached_ids)

        print("Fetching from DB...")  
        queryset = UserActivityLog.objects.filter(user=user)

        if action_type:
            queryset = queryset.filter(action_type__iexact=action_type)
        if start_date and end_date:
            queryset = queryset.filter(timestamp__range=[start_date, end_date])

        cache.set(cache_key, list(queryset.values_list("id", flat=True)), timeout=60)
        return queryset

    def perform_create(self, serializer):
        request = self.request
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')

        metadata = {
            "ip": ip_address,
            "user_agent": user_agent,
        }

        instance = serializer.save(user=request.user, metadata=metadata)

        # Invalidate all user-related caches (simplified)
        self.invalidate_user_cache(request.user.id)

    def invalidate_user_cache(self, user_id):
        """Simplified cache invalidation by pattern (if supported) or clear known keys."""
        # You can implement smarter key tracking if needed
        for key in cache.iter_keys(f"user_logs:{user_id}:*"):
            cache.delete(key)

    @action(detail=True, methods=['patch'])
    def transition(self, request, pk=None):
        activity = self.get_object()
        new_status = request.data.get('status')

        if new_status not in ['PENDING', 'IN_PROGRESS', 'DONE']:
            return Response({"error": "Invalid status"}, status=400)

        activity.status = new_status
        activity.save()

        self.invalidate_user_cache(request.user.id)
        return Response({"message": f"Status updated to {new_status}"})

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def all_logs(self, request):
        user_id = request.query_params.get('user_id')
        username = request.query_params.get('username')

        logs = UserActivityLog.objects.all()

        if user_id:
            logs = logs.filter(user__id=user_id)

        if username:
            logs = logs.filter(user__username__icontains=username)

        page = self.paginate_queryset(logs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)
