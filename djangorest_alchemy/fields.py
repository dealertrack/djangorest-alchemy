'''
Relationship field
'''
from rest_framework.relations import RelatedField
from djangorest_alchemy.inspector import primary_key, KeyNotFoundException


class AlchemyRelatedField(RelatedField):

    def __init__(self, *args, **kwargs):
        self.parent_path = kwargs.pop('path')
        super(AlchemyRelatedField, self).__init__(*args, **kwargs)

    def to_native(self, obj):
        model_name = obj.__class__.__name__.lower()

        # Try to get pk field
        # if not found, it's a child model
        # dependent on parent keys
        try:
            pk_field = primary_key(obj.__class__)
            pk_val = getattr(obj, pk_field, None)
            return self.parent_path + model_name + 's/' + str(pk_val) + '/'
        except KeyNotFoundException:
             # Use actual model name
            return self.parent_path + model_name + 's/'


class AlchemyUriField(RelatedField):
    def __init__(self, *args, **kwargs):
        self.parent_path = kwargs.pop('path')
        super(AlchemyUriField, self).__init__(*args, **kwargs)

    def to_native(self, obj):
        return self.parent_path + str(obj) + '/'
