'''
Url registrations
'''
from django.conf.urls import patterns, include, url
from rest_framework_nested import routers
from djangorest_alchemy.apibuilder import APIModelBuilder

from viewsets import CarViewSet
from viewsets import PartViewSet

from models import SessionMixin

viewset_router = routers.SimpleRouter()
viewset_router.register(r'api/cars', CarViewSet,
                        base_name='car')

# Register the child model
child_router = routers.NestedSimpleRouter(viewset_router, r'api/cars',
                                          lookup='cars')
child_router.register("parts", PartViewSet,
                      base_name='part')


# Demonstrate dynamic API builder featire
from djangorest_alchemy.model_cache import model_cache

builder = APIModelBuilder(model_cache.models, SessionMixin)
urlpatterns = patterns('',
                       url(r'^', include(viewset_router.urls)),
                       url(r'^', include(child_router.urls)),
                       url(r'^', include(builder.urls)),
                       )
