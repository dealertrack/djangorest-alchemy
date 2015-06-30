'''
Relationship field
'''
from rest_framework.relations import RelatedField

from djangorest_alchemy.inspector import KeyNotFoundException, primary_key


class AlchemyRelatedField(RelatedField):

    def __init__(self, *args, **kwargs):
        self.parent_path = kwargs.pop('path')
        super(AlchemyRelatedField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        model_name = value.__class__.__name__.lower()

        # Try to get pk field
        # if not found, it's a child model
        # dependent on parent keys
        try:
            pk_field = primary_key(value.__class__)
            pk_val = getattr(value, pk_field, None)
            return ('{parent}{model}s/{pk}/'
                    ''.format(parent=self.parent_path, model=model_name, pk=pk_val))

        except KeyNotFoundException:
             # Use actual model name
            return self.parent_path + model_name + 's/'


class AlchemyUriField(RelatedField):
    def __init__(self, *args, **kwargs):
        self.parent_path = kwargs.pop('path')
        super(AlchemyUriField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        return '{parent}{pk}/'.format(parent=self.parent_path, pk=value)
