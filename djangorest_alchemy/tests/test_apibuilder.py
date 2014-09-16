import unittest
from djangorest_alchemy.apibuilder import APIModelBuilder


class TestAPIBuilder(unittest.TestCase):

    def test_urls(self):

        class Model(object):
            pass

        class Model2(object):
            pass

        builder = APIModelBuilder([Model, Model2])
        print builder.urls