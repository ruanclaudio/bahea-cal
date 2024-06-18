from rest_framework import serializers
from django.contrib.auth.models import User

class UserInfoSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    user_email = serializers.EmailField()
    user_photo = serializers.ImageField()
    choiced_teams = serializers.DictField(child=serializers.ListField(child=serializers.EmailField()))
    time_to_match = serializers.DictField(
        child=serializers.DateTimeField()
    )
    
class Meta:
    user_model = User
    fields = ["first_name", "last_name", "user_email", "user_photo", "choiced_teams", "time_to_match"]
    
