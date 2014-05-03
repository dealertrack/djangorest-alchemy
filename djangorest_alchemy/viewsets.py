from rest_framework import viewsets
from rest_framework.response import Response
from djangorest_alchemy.serializers import AlchemyModelSerializer


class AlchemyModelViewSet(viewsets.ViewSet):
    """
    Generic SQLAlchemy viewset which calls
    methods over the specified manager_class and
    uses specified serializer_class
    """

    def list(self, request):
        assert hasattr(self, 'manager_class'), \
            "manager_class has to be specified"

        mgr = self.manager_class()
        queryset = mgr.list()
        serializer = AlchemyModelSerializer(queryset, model_class=mgr.model_class())
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        pass

    def create(self, request):
        pass

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

