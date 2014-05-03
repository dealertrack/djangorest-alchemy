from rest_framework import viewsets
from rest_framework.response import Response
from .. serializers import AlchemySerializer


class AlchemyViewSet(viewsets.ViewSet):
    """
    Generic SQLAlchemy viewset which calls
    methods over the specified manager_class and
    uses specified serializer_class
    """

    def list(self, request):
        mgr = self.manager_class()
        queryset = mgr.all()
        serializer = AlchemySerializer(queryset)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        pass

    def create(self, request):
        pass

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

