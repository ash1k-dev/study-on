from rest_framework import serializers

from study_on.courses.models import Heading


class HeadingSerializer(serializers.ModelSerializer):
    """Направление"""

    class Meta:
        model = Heading
        fields = "__all__"
