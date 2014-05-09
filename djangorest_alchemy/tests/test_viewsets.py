'''
Integration test cases for AlchemyModelViewSet
Uses Django test client
'''
from utils import SessionMixin, DeclarativeModel, ClassicalModel
from utils import CompositeKeysModel, ChildModel
from djangorest_alchemy.managers import AlchemyModelManager
from djangorest_alchemy.viewsets import AlchemyModelViewSet
from django.test import TestCase
from django.conf.urls import patterns, include, url
import unittest
import datetime

from rest_framework_nested import routers
from rest_framework import status


class DeclarativeModelManager(SessionMixin, AlchemyModelManager):
    model_class = DeclarativeModel


class DeclModelViewSet(AlchemyModelViewSet):
    manager_class = DeclarativeModelManager


class ClassicalModelManager(SessionMixin, AlchemyModelManager):
    model_class = ClassicalModel


class ClassicalModelViewSet(AlchemyModelViewSet):
    manager_class = ClassicalModelManager


class PrimaryKeyMixin(object):

    def get_other_pks(self, request):
        pks = {
            'pk1': request.META.get('PK1'),
            'pk2': request.META.get('PK2'),
        }

        return pks


class ModelManager(SessionMixin, AlchemyModelManager):
    model_class = CompositeKeysModel


class ModelViewSet(PrimaryKeyMixin, AlchemyModelViewSet):
    manager_class = ModelManager


class ChildModelManager(SessionMixin, AlchemyModelManager):
    model_class = ChildModel


class ChildModelViewSet(AlchemyModelViewSet):
    manager_class = ChildModelManager

viewset_router = routers.SimpleRouter()
viewset_router.register(r'api/declmodels', DeclModelViewSet, base_name='test-decl')
viewset_router.register(r'api/clsmodels', ClassicalModelViewSet,
                        base_name='test-cls')
viewset_router.register(r'api/compositemodels', ModelViewSet,
                        base_name='test-composite')

child_router = routers.NestedSimpleRouter(viewset_router, r'api/declmodels', lookup='declmodels')
child_router.register("childmodels", ChildModelViewSet, base_name='test-childmodel')

urlpatterns = patterns('',
                       url(r'^', include(viewset_router.urls)),
                       url(r'^', include(child_router.urls)),
                       )


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
        self.assertTrue(isinstance(resp.data['bigintfield'], (int, long)))

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

    def test_with_multiple_pk_retrieve(self):
        resp = self.client.get('/api/compositemodels/1/',
                               PK1='ABCD', PK2='WXYZ')
        self.assertTrue(resp.status_code is status.HTTP_200_OK)
        self.assertTrue(not type(resp.data) is list)
        self.assertEqual(resp.data['id'], 1)
        self.assertEqual(resp.data['pk1'], 'ABCD')
        self.assertEqual(resp.data['pk2'], 'WXYZ')

    def test_hierarchical_multiple_pk_retrieve(self):
        resp = self.client.get('/api/declmodels/1/childmodels/2/',
                               PK1='ABCD', PK2='WXYZ')
        self.assertTrue(resp.status_code is status.HTTP_200_OK)

