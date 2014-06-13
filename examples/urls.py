'''
Url registrations
'''
from django.conf.urls import patterns, include, url
from rest_framework_nested import routers

from viewsets import CarViewSet
from viewsets import PartViewSet

viewset_router = routers.SimpleRouter()
viewset_router.register(r'api/cars', CarViewSet,
                        base_name='car')

# Register the child model
child_router = routers.NestedSimpleRouter(viewset_router, r'api/cars',
                                          lookup='cars')
child_router.register("parts", PartViewSet,
                      base_name='part')

urlpatterns = patterns('',
                       url(r'^', include(viewset_router.urls)),
                       url(r'^', include(child_router.urls)),
                       )
