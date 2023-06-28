from djoser.serializers import UserCreateSerializer as BaseUserCreateSerialize


class UserCreateSerializer(BaseUserCreateSerialize):
    class Meta(BaseUserCreateSerialize.Meta):
        fields = ["id", "username", "password", "email", "first_name", "last_name"]
