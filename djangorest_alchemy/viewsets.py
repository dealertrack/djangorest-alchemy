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

    def get_other_pks(self, request):
        '''
        Return default empty {}
        '''
        return {}

    def get_pks(self, request, **kwargs):
        '''
        Return list of pks
        from the URI
        e.g. /models/pk1/childmodel/pk2 return back [pk1, pk2]
        '''
        return kwargs.values()

    def list(self, request):
        assert hasattr(self, 'manager_class'), \
            "manager_class has to be specified"

        mgr = self.manager_class()
        queryset = mgr.list()
        serializer = AlchemyModelSerializer(queryset,
                                            model_class=mgr.model_class(),
                                            context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, **kwargs):
        assert hasattr(self, 'manager_class'), \
            "manager_class has to be specified"

        mgr = self.manager_class(headers=self.get_other_pks(request))
        queryset = mgr.retrieve(self.get_pks(request, **kwargs))

        serializer = AlchemyModelSerializer(queryset, model_class=mgr.model_class(),
                                            context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        pass

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

