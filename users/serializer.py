from rest_framework import serializers
from django.contrib.auth.models import User

class UserInfoSerializer(serializers.Serializer):
    id = serializers.CharField()
    email = serializers.EmailField()
    verified_email = serializers.BooleanField()
    name = serializers.CharField()
    given_name = serializers.CharField()
    family_name = serializers.CharField()
    picture = serializers.CharField()
    
    class Meta:
        user_model = User
        fields = ["id", "email", "verified_email", "name", "given_name", "family_name", "picture"]
    
# {
#     "id": "109776696914646781435",
#     "email": "ruanclaudio4@gmail.com",
#     "verified_email": true,
#     "name": "Ruan Cláudio",
#     "given_name": "Ruan",
#     "family_name": "Cláudio",
#     "picture": "https://lh3.googleusercontent.com/a/ACg8ocKoJXxaqmOY3mvQBIKRAxigf4fqC-H0g-6X0t051UYVPfZeaqQr=s96-c"
# }
