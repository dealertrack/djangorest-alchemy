'''
Base AlchemyModelSerializer which provides the mapping between
SQLALchemy and DRF fields to serialize/deserialize objects
'''
from rest_framework import serializers
from rest_framework.relations import *
from rest_framework.fields import *
from sqlalchemy.types import *
from sqlalchemy import *
from django.utils.datastructures import SortedDict
from djangorest_alchemy.fields import AlchemyRelatedField
# inspect introduced in 0.8
#from sqlalchemy import inspect
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.properties import RelationshipProperty, ColumnProperty


class AlchemyModelSerializer(serializers.Serializer):
    """
    Alchemy -> DRF field serializer
    """

    field_mapping = {
        String: CharField,
        INTEGER: IntegerField,
        SMALLINT: IntegerField,
        BIGINT: IntegerField,
        VARCHAR: CharField,
        CHAR: CharField,
        TIMESTAMP: DateTimeField,
        Float: FloatField,
        BigInteger: IntegerField,
        Numeric: IntegerField,
        DateTime: DateTimeField,
        Boolean: BooleanField,
    }

    def __init__(self, *args, **kwargs):
        assert "model_class" in kwargs, \
            "model_class should be passed"

        self.cls = kwargs.pop('model_class')
        super(AlchemyModelSerializer, self).__init__(*args, **kwargs)

    def get_default_fields(self):

        assert not self.cls is None, 'model_class needs to be specified'

        ret = SortedDict()

        mapper = class_mapper(self.cls.__class__)

        # Get all the Column fields
        for col_prop in mapper.iterate_properties:
            if isinstance(col_prop, ColumnProperty):
                field_nm = str(col_prop).split('.')[1]
                field_cls = col_prop.columns[0].type.__class__

                assert field_cls in self.field_mapping, \
                    "Field %s has not been mapped"

                ret[field_nm] = self.field_mapping[field_cls]()

        # Get all the relationship fields
        for rel_prop in mapper.iterate_properties:
            if isinstance(rel_prop, RelationshipProperty):
                field_nm = str(rel_prop).split('.')[1]
                # many becomes same as uselist so that
                # RelatedField can iterate over the queryset
                ret[field_nm] = AlchemyRelatedField(source=field_nm,
                                                    many=rel_prop.uselist,
                                                    request=self.context['request'])

        return ret



