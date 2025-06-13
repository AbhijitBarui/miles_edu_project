from rest_framework import serializers
from .models import UserActivityLog

class UserActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivityLog
        fields = '__all__'
        read_only_fields = ['user', 'timestamp']

    def validate_status(self, value):
        valid_choices = ['PENDING', 'IN_PROGRESS', 'DONE']
        if value not in valid_choices:
            raise serializers.ValidationError("Invalid status")
        return value
