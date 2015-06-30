'''
Base AlchemyModelSerializer which provides the mapping between
SQLALchemy and DRF fields to serialize/deserialize objects
'''
from django.utils.datastructures import SortedDict
from rest_framework import serializers
from rest_framework.fields import (
    BooleanField,
    CharField,
    DateTimeField,
    DecimalField,
    FloatField,
    IntegerField,
)
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.properties import ColumnProperty, RelationshipProperty
from sqlalchemy.types import (
    BIGINT,
    CHAR,
    CLOB,
    DATE,
    DECIMAL,
    INTEGER,
    SMALLINT,
    TIMESTAMP,
    VARCHAR,
    BigInteger,
    Boolean,
    DateTime,
    Float,
    Numeric,
    String,
)

from djangorest_alchemy.fields import AlchemyRelatedField, AlchemyUriField

from .inspector import KeyNotFoundException, primary_key


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
        DATE: DateTimeField,
        Float: FloatField,
        BigInteger: IntegerField,
        Numeric: IntegerField,
        DateTime: DateTimeField,
        Boolean: BooleanField,
        CLOB: CharField,
        DECIMAL: DecimalField,
    }

    def __init__(self, *args, **kwargs):
        assert "model_class" in kwargs, \
            "model_class should be passed"
        assert 'request' in kwargs['context'], \
            "Context must contain request object"

        self.cls = kwargs.pop('model_class')
        super(AlchemyModelSerializer, self).__init__(*args, **kwargs)

    def get_fields(self):

        ret = SortedDict()

        mapper = class_mapper(self.cls.__class__)

        r = self.context['request']
        try:
            # URI field for get pk field
            pk_field = primary_key(self.cls.__class__)
            ret['href'] = AlchemyUriField(source=pk_field,
                                          path=r.build_absolute_uri(r.path),
                                          read_only=True)
        except KeyNotFoundException:
            pass

        # Get all the Column fields
        for col_prop in mapper.iterate_properties:
            if isinstance(col_prop, ColumnProperty):
                field_nm = str(col_prop).split('.')[1]
                field_cls = col_prop.columns[0].type.__class__

                assert field_cls in self.field_mapping, \
                    "Field %s has not been mapped" % field_cls

                ret[field_nm] = self.field_mapping[field_cls]()

        # Get all the relationship fields
        for rel_prop in mapper.iterate_properties:
            if isinstance(rel_prop, RelationshipProperty):
                field_nm = str(rel_prop).split('.')[1]
                # many becomes same as uselist so that
                # RelatedField can iterate over the queryset
                kwargs = dict(
                    path=r.build_absolute_uri(r.path),
                    read_only=True
                )
                if rel_prop.uselist:
                    kwargs['many'] = True
                ret[field_nm] = AlchemyRelatedField(**kwargs)

        return ret


class AlchemyListSerializer(AlchemyModelSerializer):
    def get_fields(self):
        ret = SortedDict()

        try:
            # URI field for get pk field
            pk_field = primary_key(self.cls.__class__)

            request = self.context['request']
            ret["href"] = AlchemyUriField(
                source=pk_field,
                path=request.build_absolute_uri(request.path),
                read_only=True,
            )
        except KeyNotFoundException:
            return super(AlchemyListSerializer, self).get_fields()

        return ret
