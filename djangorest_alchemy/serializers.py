'''
Base AlchemyModelSerializer which provides the mapping between
SQLALchemy and DRF fields to serialize/deserialize objects
'''
from rest_framework import serializers
#from rest_framework.relations import *
from rest_framework.fields import (CharField, IntegerField, DateTimeField,
                                   FloatField, BooleanField)
from sqlalchemy.types import (String, INTEGER, SMALLINT, BIGINT, VARCHAR,
                              CHAR, TIMESTAMP, DATE, Float, BigInteger,
                              Numeric, DateTime, Boolean)
#from sqlalchemy import *
from django.utils.datastructures import SortedDict
from djangorest_alchemy.fields import AlchemyRelatedField, AlchemyUriField
# inspect introduced in 0.8
#from sqlalchemy import inspect
from sqlalchemy.orm import class_mapper
from inspector import primary_key, KeyNotFoundException
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
        DATE: DateTimeField,
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

    #def to_native(self, obj):
    #    native = super(AlchemyModelSerializer, self).to_native(obj)
    #    import pdb
    #    pdb.set_trace()
    #    return native

    def get_default_fields(self):

        ret = SortedDict()

        mapper = class_mapper(self.cls.__class__)

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
                r = self.context['request']
                # many becomes same as uselist so that
                # RelatedField can iterate over the queryset
                ret[field_nm] = AlchemyRelatedField(source=field_nm,
                                                    many=rel_prop.uselist,
                                                    path=r.build_absolute_uri(
                                                        r.path))

        # Get all the property fields
        #for prop, value in self.cls.__dict__.iteritems():
        #    import pdb
        #    pdb.set_trace()
        #    if isinstance(value, property):
        #        ret[prop] = self.field_mapping[value.type.__class__]

        # Below can be conditional based on a flag
        # if we want to use URI instead of actual id

        # Generate uri field for pk field
        #pk_field = primary_key(self.cls.__class__)
        # Remove the pk from the url and pass the base path
        #ret[pk_field] = AlchemyUriField(source=pk_field,
        #                                path='/'.join(
        #self.context['request'].path.split('/')[:-2]) + '/')

        return ret


class AlchemyListSerializer(AlchemyModelSerializer):
    def get_default_fields(self):
        ret = SortedDict()

        try:
            # URI field for get pk field
            pk_field = primary_key(self.cls.__class__)
        except KeyNotFoundException:
            return ret

        request = self.context['request']
        ret[pk_field] = AlchemyUriField(source=pk_field,
                                        path=request.build_absolute_uri(
                                            request.path))

        return ret
