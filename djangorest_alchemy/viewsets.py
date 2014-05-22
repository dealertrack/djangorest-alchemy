'''
Base AlchemyViewSet which provides
the necessary plumbing to interface with
AlchemyModelSerializer and AlchemyModelManager
'''
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from djangorest_alchemy.serializers import AlchemyModelSerializer
from djangorest_alchemy.serializers import AlchemyListSerializer
from djangorest_alchemy.mixins import MultipleObjectMixin

from django.core.paginator import InvalidPage


class AlchemyModelViewSet(MultipleObjectMixin, viewsets.ViewSet):
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

        :param request: REST request object
        :return: dict

        '''
        return {}

    def get_pks(self, request, **kwargs):
        '''
        Return list of pks
        from the keyword args
        e.g. /models/pk1/childmodel/pk2 return back [pk1, pk2]

        :param request: REST request object
        :kwargs kwargs: URI keyword args
        :return: List e.g. [pk1, pk2]
        '''
        return kwargs.values()

    def list(self, request, **kwargs):
        '''
        Returns back serialized list of objects URIs

        :return: json
            [
                {
                    "pk": "http://server/api/models/pk/"
                }
            ]

        Note::

            * URI contains the same pk field
            * Complete URI with server/port is returned back
        '''

        mgr = self.manager_factory(context={'request': request})

        queryset = mgr.list(other_pks=self.get_other_pks(request),
                            filters=request.QUERY_PARAMS)

        if self.paginate_by:
            try:
                queryset = self.get_page(queryset)
            except InvalidPage:
                return Response({}, status.HTTP_400_BAD_REQUEST)

        serializer = AlchemyListSerializer(queryset,
                                           model_class=mgr.model_class(),
                                           context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, **kwargs):
        '''
        Retrieve returns back serialized object.

        :return: json
            {
                "pk": "value",
                "field": "value"
                "childmodel": "http://serv/api/parentmodels/pk/childmodels/pk"
            }

        Note::

            As of now, only SQLAlchemy mapper properties are returned
            No other fields or properties are serialized. You will need
            to override retrieve and provide your own implementation to
            query those additional properties for now.
        '''

        mgr = self.manager_factory(context={'request': request})

        queryset = mgr.retrieve(self.get_pks(request, **kwargs),
                                other_pks=self.get_other_pks(request))

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
