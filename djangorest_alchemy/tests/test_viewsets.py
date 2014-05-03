from utils import SessionMixin, TestModel
from djangorest_alchemy.managers import AlchemyModelManager
from djangorest_alchemy.viewsets import AlchemyModelViewSet
from django.test import TestCase

from rest_framework import routers
from rest_framework import status


# SessionMixin just allows us to instantiate the
# SA session
class ModelManager(SessionMixin, AlchemyModelManager):
    model_class = TestModel


class ModelViewSet(AlchemyModelViewSet):
    manager_class = ModelManager

viewset_router = routers.DefaultRouter()
viewset_router.register(r'api/testmodels', ModelViewSet, base_name='test')
urlpatterns = viewset_router.urls


class TestAlchemyViewSet(TestCase):

    def test_list(self):
        resp = self.client.get('/api/testmodels/')
        self.assertTrue(resp.status_code is status.HTTP_200_OK)
        self.assertTrue(type(resp.data) is list)
        print resp
