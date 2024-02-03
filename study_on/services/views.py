from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet


class ViewSetSerializerMixin:
    create_serializer_class: serializers.Serializer | None = None
    update_serializer_class: serializers.Serializer | None = None
    list_serializer_class: serializers.Serializer | None = None

    def _get_serializer_class(
        self,
        *args,
        **kwargs,
    ):
        if self.action == "create":  # type: ignore
            return self.create_serializer_class
        if self.action in {"update", "partial_update"}:  # type: ignore
            return self.update_serializer_class or self.create_serializer_class
        if self.action == "list":  # type: ignore
            return self.list_serializer_class
        return None

    def get_serializer_class(self):
        serializer_class = self._get_serializer_class()
        if serializer_class:
            return serializer_class
        return super().get_serializer_class()  # type: ignore


class BaseModelViewSet(ModelViewSet, ViewSetSerializerMixin):
    pass
