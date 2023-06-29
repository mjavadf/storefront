from djoser.serializers import UserCreateSerializer as BaseUserCreateSerialize
from djoser.serializers import UserSerializer as BaseUserSerializer


class UserCreateSerializer(BaseUserCreateSerialize):
    class Meta(BaseUserCreateSerialize.Meta):
        fields = ["id", "username", "password", "email", "first_name", "last_name"]
        
        
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = fields = ["id", "username", "email", "first_name", "last_name"]
