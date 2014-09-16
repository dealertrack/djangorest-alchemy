'''
Url registrations
'''
from django.conf.urls import patterns, include, url
from rest_framework_nested import routers
from djangorest_alchemy.apibuilder import APIModelBuilder

from viewsets import CarViewSet
from viewsets import PartViewSet

from models import Car, Part, SessionMixin

#viewset_router = routers.SimpleRouter()
#viewset_router.register(r'api/cars_foo', CarViewSet,
#                        base_name='car')

# Register the child model
#child_router = routers.NestedSimpleRouter(viewset_router, r'api/cars_foo',
#                                          lookup='cars')
#child_router.register("parts", PartViewSet,
#                      base_name='part')


builder = APIModelBuilder([Car, Part], SessionMixin)
urlpatterns = patterns('',
                       #url(r'^', include(viewset_router.urls)),
                       #url(r'^', include(child_router.urls)),
                       url(r'^', include(builder.urls)),
                       )
