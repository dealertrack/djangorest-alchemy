import unittest

import mock

from djangorest_alchemy.apibuilder import APIModelBuilder


class TestAPIBuilder(unittest.TestCase):

    def test_urls(self):
        """
        Test basic urls property
        """

        class Model(object):
            pass

        class Model2(object):
            pass

        class SessionMixin(object):
            def __init__(self):
                self.session = mock.Mock()

        builder = APIModelBuilder([Model, Model2], SessionMixin)
        self.assertIsNotNone(builder.urls)
