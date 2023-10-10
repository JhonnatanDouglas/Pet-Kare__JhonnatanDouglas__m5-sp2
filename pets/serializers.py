from rest_framework import serializers
from .models import Gender
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer


def validate_sex(value):
    if len(value) > 20:
        raise serializers.ValidationError(
            f"Ensure this field has no more than 20 characters."
        )


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        validators=[validate_sex],
        choices=Gender.choices,
        default=Gender.NOT_INFORMED,
    )

    group = GroupSerializer()
    traits = TraitSerializer(many=True)
