from rest_framework import serializers
from django.contrib.auth.models import User

class UserInfoSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    photo = serializers.ImageField()
    selected_teams = serializers.DictField(child=serializers.ListField(child=serializers.EmailField()))
    notify_before = serializers.DictField(
        child=serializers.DateTimeField()
    )
    
class Meta:
    user_model = User
    fields = ["first_name", "last_name", "user_email", "user_photo", "choiced_teams", "time_to_match"]
    
