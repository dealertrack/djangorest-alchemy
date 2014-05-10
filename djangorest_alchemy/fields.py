'''
Relationship field
'''
from rest_framework.relations import *


class AlchemyRelatedField(RelatedField):

    def __init__(self, *args, **kwargs):
        self.parent_path = kwargs.pop('path')
        super(AlchemyRelatedField, self).__init__(*args, **kwargs)

    def to_native(self, obj):
        model_name = obj.__class__.__name__.lower()
        # guess the pk of the model
        # using <modelname>_id convention if found
        pk_val = getattr(obj, model_name + '_id', None)
        return self.parent_path + model_name + 's/' + str(pk_val) + '/'


class AlchemyUriField(RelatedField):
    def __init__(self, *args, **kwargs):
        self.parent_path = kwargs.pop('path')
        super(AlchemyUriField, self).__init__(*args, **kwargs)

    def to_native(self, obj):
        return self.parent_path + str(obj) + '/'
