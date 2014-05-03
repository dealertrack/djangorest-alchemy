from rest_framework import serializers
from rest_framework.fields import *
from sqlalchemy.types import *
from sqlalchemy import *
from django.utils.datastructures import SortedDict


class AlchemyModelSerializer(serializers.Serializer):
    """
    Alchemy -> DRF field serializer
    """

    field_mapping = {
        String: CharField,
        INTEGER: IntegerField
    }

    def __init__(self, *args, **kwargs):
        assert "model_class" in kwargs, \
            "model_class should be passed"

        self.cls = kwargs.pop('model_class')
        super(AlchemyModelSerializer, self).__init__(*args, **kwargs)

    def get_default_fields(self):

        assert not self.cls is None, 'model_class needs to be specified'

        ret = SortedDict()

        for field in self.cls.__table__.columns:
            ret[field.name] = self.field_mapping[field.type.__class__]()

        return ret




