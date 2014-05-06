'''
Base AlchemyViewSet which provides
the necessary plumbing to interface with
AlchemyModelSerializer and AlchemyModelManager
'''
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
        assert hasattr(self, 'manager_class'), \
            "manager_class has to be specified"

        mgr = self.manager_class()

        if hasattr(self, 'get_other_pks'):
            pks = self.get_other_pks(request)
            new = pks.values()
            new.sort()  # This sort is a hack for now, need to use
            # correct PK order from the model itself
            all_pks = tuple(pk) + tuple(new)
            queryset = mgr.retrieve(all_pks)
        else:
            queryset = mgr.retrieve(pk)

        serializer = AlchemyModelSerializer(queryset, model_class=mgr.model_class())
        return Response(serializer.data)

    def create(self, request):
        pass

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

