from rest_framework import serializers

from study_on.courses.models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ["course", "student"]
