'''
Base AlchemyViewSet which provides
the necessary plumbing to interface with
AlchemyModelSerializer and AlchemyModelManager
'''
from rest_framework import viewsets
from rest_framework.response import Response
from djangorest_alchemy.serializers import AlchemyModelSerializer, AlchemyListSerializer


class AlchemyModelViewSet(viewsets.ViewSet):
    """
    Generic SQLAlchemy viewset which calls
    methods over the specified manager_class and
    uses specified serializer_class
    """

    def manager_factory(self, *args, **kwargs):
        '''
        Factory method for instantiating manager class
        Override to return back your instance
        '''
        assert hasattr(self, 'manager_class'), \
            "manager_class has to be specified"
        return self.manager_class(*args, **kwargs)

    def get_other_pks(self, request):
        '''
        Return default empty {}
        Override to return back your primary keys
        from other source (possibly from headers)
        '''
        return {}

    def get_pks(self, request, **kwargs):
        '''
        Return list of pks
        from the keyword args
        e.g. /models/pk1/childmodel/pk2 return back [pk1, pk2]
        '''
        return kwargs.values()

    def list(self, request):

        mgr = self.manager_factory(context={'request': request})
        queryset = mgr.list(other_pks=self.get_other_pks(request))
        serializer = AlchemyListSerializer(queryset,
                                           model_class=mgr.model_class(),
                                           context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, **kwargs):

        mgr = self.manager_factory(context={'request': request})
        queryset = mgr.retrieve(self.get_pks(request, **kwargs), other_pks=self.get_other_pks(request))

        serializer = AlchemyModelSerializer(queryset,
                                            model_class=mgr.model_class(),
                                            context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        pass

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

