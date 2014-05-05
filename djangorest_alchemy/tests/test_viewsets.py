'''
Integration test cases for AlchemyModelViewSet
Uses Django test client
'''
from utils import SessionMixin, DeclarativeModel, ClassicalModel
from djangorest_alchemy.managers import AlchemyModelManager
from djangorest_alchemy.viewsets import AlchemyModelViewSet
from django.test import TestCase
import datetime

from rest_framework import routers
from rest_framework import status


class DeclarativeModelManager(SessionMixin, AlchemyModelManager):
    model_class = DeclarativeModel


class DeclModelViewSet(AlchemyModelViewSet):
    manager_class = DeclarativeModelManager


class ClassicalModelManager(SessionMixin, AlchemyModelManager):
    model_class = ClassicalModel


class ClassicalModelViewSet(AlchemyModelViewSet):
    manager_class = DeclarativeModelManager


viewset_router = routers.DefaultRouter()
viewset_router.register(r'api/declmodels', DeclModelViewSet, base_name='test')
viewset_router.register(r'api/clsmodels', ClassicalModelViewSet,
                        base_name='test')
urlpatterns = viewset_router.urls


class TestAlchemyViewSet(TestCase):

    def test_decl_list(self):
        resp = self.client.get('/api/declmodels/')
        self.assertTrue(resp.status_code is status.HTTP_200_OK)
        self.assertTrue(type(resp.data) is list)

    def test_decl_retrieve(self):
        resp = self.client.get('/api/declmodels/1/')
        self.assertTrue(resp.status_code is status.HTTP_200_OK)
        self.assertTrue(not type(resp.data) is list)
        self.assertEqual(resp.data['id'], 1)
        self.assertEqual(resp.data['field'], 'test')
        self.assertIsInstance(resp.data['datetime'], datetime.datetime)
        self.assertIsInstance(resp.data['floatfield'], float)
        self.assertIsInstance(resp.data['bigintfield'], long)

    def test_classical_list(self):
        resp = self.client.get('/api/clsmodels/')
        self.assertTrue(resp.status_code is status.HTTP_200_OK)
        self.assertTrue(type(resp.data) is list)

    def test_classical_retrieve(self):
        resp = self.client.get('/api/clsmodels/1/')
        self.assertTrue(resp.status_code is status.HTTP_200_OK)
        self.assertTrue(not type(resp.data) is list)
        self.assertEqual(resp.data['id'], 1)
        self.assertEqual(resp.data['field'], 'test')



