from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Room


class RoomSerializer(serializers.Serializer):

    user = UserSerializer()

    class Meta:
        model = Room
        exclude = ("modified",)
        read_only_fields = ("user", "id", "created", "updated")  # don't validate

    # validate all
    def validate(self, data):
        if self.instance:
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)
        else:
            check_in = data.get("check_in")
            check_out = data.get("check_out")
            if check_in == check_out:
                raise serializers.ValidationError("Not enough time between changes")
        return data

    # validate specific field

    # def validate_field(self, value):
    #     if something:
    #         return value
    #     else:
    #         raise serializers.ValidationError("value error")