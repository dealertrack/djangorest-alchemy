'''
Integration test cases for AlchemyModelViewSet
Uses Django test client
'''
import unittest

import mock
import six
from django.conf.urls import include, patterns, url
from django.test import TestCase
from rest_framework import status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework_nested import routers

from djangorest_alchemy.managers import AlchemyModelManager
from djangorest_alchemy.mixins import ManagerMixin
from djangorest_alchemy.viewsets import AlchemyModelViewSet

from .utils import (
    ChildModel,
    ClassicalModel,
    CompositeKeysModel,
    DeclarativeModel,
    SessionMixin,
)


RESULTS_KEY = "results"
COUNT_KEY = "count"
PAGE_KEY = "page"


class PrimaryKeyMixin(object):
    def get_other_pks(self, request):
        pks = {
            'pk1': request.META.get('PK1'),
            'pk2': request.META.get('PK2'),
        }

        return pks


class DeclarativeModelManager(SessionMixin, AlchemyModelManager):
    model_class = DeclarativeModel

    def do_something(self, data, pk=None, **kwargs):
        pass


class DeclModelViewSet(AlchemyModelViewSet):
    manager_class = DeclarativeModelManager
    paginate_by = 25

    def list(self, request, **kwargs):
        return super(DeclModelViewSet, self).list(request, **kwargs)

    @detail_route(methods=['POST'])
    def do_something(self, request, pk=None, **kwargs):
        mgr = self.manager_factory()
        # Delegate to manager method
        mgr.do_something(request.data, pk=pk, **kwargs)
        return Response({'status': 'did_something'}, status=status.HTTP_200_OK)


class ClassicalModelManager(SessionMixin, AlchemyModelManager):
    model_class = ClassicalModel


class ClassicalModelViewSet(AlchemyModelViewSet):
    manager_class = ClassicalModelManager


class ModelManager(SessionMixin, AlchemyModelManager):
    model_class = CompositeKeysModel


class ModelViewSet(PrimaryKeyMixin, AlchemyModelViewSet):
    manager_class = ModelManager


class ChildModelManager(SessionMixin, AlchemyModelManager):
    model_class = ChildModel


class ChildModelViewSet(AlchemyModelViewSet):
    manager_class = ChildModelManager


viewset_router = routers.SimpleRouter()
viewset_router.register(r'api/declmodels', DeclModelViewSet,
                        base_name='test-decl')
viewset_router.register(r'api/clsmodels', ClassicalModelViewSet,
                        base_name='test-cls')
viewset_router.register(r'api/compositemodels', ModelViewSet,
                        base_name='test-composite')

# Register the child model
child_router = routers.NestedSimpleRouter(viewset_router, r'api/declmodels',
                                          lookup='declmodels')
child_router.register("childmodels", ChildModelViewSet,
                      base_name='test-childmodel')

urlpatterns = patterns('',
                       url(r'^', include(viewset_router.urls)),
                       url(r'^', include(child_router.urls)),
                       )


class TestAlchemyViewSetIntegration(TestCase):
    def test_decl_list(self):
        resp = self.client.get('/api/declmodels/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp.data, dict)
        self.assertTrue(len(resp.data[RESULTS_KEY]) == 1)
        self.assertTrue(resp.data[COUNT_KEY] == 1)
        self.assertTrue(resp.data[PAGE_KEY] == 25)

    def test_decl_retrieve(self):
        resp = self.client.get('/api/declmodels/1/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp.data, dict)
        self.assertEqual(resp.data['declarativemodel_id'], 1)
        self.assertEqual(resp.data['field'], 'test')
        self.assertIsInstance(resp.data['datetime'], six.string_types)
        self.assertIsInstance(resp.data['floatfield'], float)
        self.assertIsInstance(resp.data['bigintfield'], six.integer_types)

    def test_classical_list(self):
        resp = self.client.get('/api/clsmodels/?field=test')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp.data, dict)
        self.assertTrue(len(resp.data[RESULTS_KEY]) == 1)

    def test_classical_retrieve(self):
        resp = self.client.get('/api/clsmodels/1/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp.data, dict)
        self.assertEqual(resp.data['classicalmodel_id'], 1)
        self.assertEqual(resp.data['field'], 'test')

    #
    # Composite key tests
    #

    def test_with_multiple_pk_retrieve(self):
        resp = self.client.get('/api/compositemodels/1/',
                               PK1='ABCD', PK2='WXYZ')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp.data, dict)
        self.assertEqual(resp.data['compositekeysmodel_id'], 1)
        self.assertEqual(resp.data['pk1'], 'ABCD')
        self.assertEqual(resp.data['pk2'], 'WXYZ')

    def test_hierarchical_multiple_pk_retrieve(self):
        resp = self.client.get('/api/declmodels/1/childmodels/2/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['childmodel_id'], 2)
        self.assertEqual(resp.data['parent_id'], 1)

    #
    # Filter and pagination tests
    #

    def test_basic_filter(self):
        resp = self.client.get('/api/declmodels/?field=test')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp.data, dict)
        self.assertTrue(len(resp.data[RESULTS_KEY]) == 1)

    def test_invalid_filter(self):
        resp = self.client.get('/api/declmodels/?field=invalid')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp.data, dict)
        self.assertTrue(len(resp.data[RESULTS_KEY]) == 0)

    def test_basic_pagination(self):
        resp = self.client.get('/api/declmodels/?page=1')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp.data, dict)
        self.assertTrue(len(resp.data[RESULTS_KEY]) == 1)

        resp = self.client.get('/api/declmodels/?page=last')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp.data, dict)
        self.assertTrue(len(resp.data[RESULTS_KEY]) == 1)

    def test_invalid_pagination(self):
        resp = self.client.get('/api/declmodels/?page=foo')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    #
    # Action methods
    #

    def test_action_method(self):
        resp = self.client.post('/api/declmodels/1/do_something/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


class TestAlchemyViewSetUnit(unittest.TestCase):
    def test_manager_factory(self):
        '''
        Test if manager_factory returns back appropriate instance
        This shows how you can override manager_factory
        and instantiate your own manager
        '''

        class MockManager(AlchemyModelManager):
            model_class = mock.Mock()

            def __init__(self, *args, **kwargs):
                self.session = mock.Mock()
                super(MockManager, self).__init__(*args, **kwargs)

        class MockViewSet(AlchemyModelViewSet):
            def manager_factory(self, *args, **kwargs):
                return MockManager()

        viewset = MockViewSet()
        self.assertIsInstance(viewset.manager_factory(), MockManager)

    def test_get_other_pks(self):
        '''
        Test override get_other_pks
        and assert return value
        '''
        # Test overriding
        class MockViewSet(AlchemyModelViewSet):
            def get_other_pks(self, request):
                return {'pk1': 'value'}

        viewset = MockViewSet()
        pks = viewset.get_other_pks(mock.Mock())
        self.assertIsNotNone(pks)
        self.assertIn('pk1', pks)

        # Tese default implementation
        class MockViewSet(AlchemyModelViewSet):
            pass

        viewset = MockViewSet()
        pks = viewset.get_other_pks(mock.Mock())
        self.assertIsNotNone(pks)
        self.assertIsInstance(pks, dict)

    def test_action_methods_manager_mixin(self):
        '''
        Test if action methods specified on managers using action_methods
        class field are registered with viewset
        '''

        class MockManager(SessionMixin, AlchemyModelManager):
            model_class = mock.Mock()
            action_methods = {'method_name': ['POST', 'DELETE']}

            def method_name(self, data, pk=None, **kwargs):
                return {'status': 'created'}

        class MockViewSet(viewsets.ViewSet, ManagerMixin):
            manager_class = MockManager

        viewset = MockViewSet()
        self.assertTrue(hasattr(viewset, 'method_name'))

        method = getattr(viewset, 'method_name')
        # DRF looks for methods with this attr
        self.assertTrue(hasattr(method, 'bind_to_methods'))

    def test_status_action_methods_manager(self):
        '''
        Test if action methods return appropriate status
        '''

        class MockManager(SessionMixin, AlchemyModelManager):
            model_class = mock.Mock()
            action_methods = {
                'action_method': ['POST', 'DELETE'],
                'accept_method': ['POST'],
                'update_method': ['POST']
            }

            def action_method(self, data, *args, **kwargs):
                '''
                Return back status as 'created' and data in 'result' key
                '''
                return {'status': 'created', 'result': 'some_data'}

            def accept_method(self, data, pk=None, **kwargs):
                """
                assert if self.session is available
                """
                assert self.session is not None

                return {'status': 'accepted'}

            def update_method(self, data, pk=None, **kwargs):
                return {'status': 'updated'}

        class MockViewSet(AlchemyModelViewSet, ManagerMixin):
            manager_class = MockManager

        mock_request = mock.Mock()
        mock_request.data = {}

        viewset = MockViewSet()
        r = viewset.action_method(mock_request)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = viewset.accept_method(mock_request)
        self.assertEqual(r.status_code, status.HTTP_202_ACCEPTED)

        r = viewset.update_method(mock_request)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_action_methods_manager_exception(self):
        '''
        Test if action methods specified on managers raise exceptions
        and are caught properly
        '''

        class MockManager(SessionMixin, AlchemyModelManager):
            model_class = mock.Mock()
            action_methods = {'method_name': ['POST', 'DELETE']}

            def method_name(self, data, pk=None, **kwargs):
                raise ValueError('Dummy exception')

        class MockViewSet(AlchemyModelViewSet, ManagerMixin):
            manager_class = MockManager

        mock_request = mock.Mock()
        mock_request.data = {}

        viewset = MockViewSet()
        self.assertRaises(ValueError, viewset.method_name, mock_request)
