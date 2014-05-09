'''
Base for interfacing with SQLAlchemy
Provides the necessary plumbing for CRUD
using SA session
'''
from sqlalchemy.orm import class_mapper


def class_keys(cls):
    """This is a utility function to get the attribute names for
    the primary keys of a class

    # >>> class_keys(Deal)
    # >>> ('dealer_code', 'deal_jacket_id', 'deal_id')
    """
    reverse_map = {}
    for name, attr in cls.__dict__.items():
        try:
            reverse_map[attr.property.columns[0].name] = name
        except:
            pass
    mapper = class_mapper(cls)
    return tuple(reverse_map[key.name] for key in mapper.primary_key)


class AlchemyModelManager(object):

    def __init__(self, *args, **kwargs):
        '''
        self.session is expected to be initialized
        by the derived class
        '''
        if 'headers' in kwargs:
            self.context = kwargs.pop('headers')

        super(AlchemyModelManager, self).__init__(*args, **kwargs)

        assert hasattr(self, 'session'), "session is expected"
        assert self.session is not None, "session must be initialized" \
                                         "by the derived class"

        self.cls = self.model_class

    def list(self, filters=None):
        return self.session.query(self.cls).all()

    def retrieve(self, pks):

        newargs = list(pks)
        for key in class_keys(self.cls):
            if key in self.context:
                newargs.append(self.context[key])

        return self.session.query(self.cls).get(newargs)

