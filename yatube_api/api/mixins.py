from rest_framework import mixins, viewsets


class ListCreateViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """Кастомный ViewSet: разрешает только получение списка и создание."""


class PerformCreateUserMixin:
    """
    Миксин для автоматической подстановки
    request.user при создании объекта.
    """

    user_field_name = "user"

    def perform_create(self, serializer):
        kwargs = {self.user_field_name: self.request.user}
        serializer.save(**kwargs)
