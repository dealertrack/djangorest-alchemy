'''
Base for interfacing with SQLAlchemy
Provides the necessary plumbing for CRUD
using SA session
'''
from sqlalchemy.orm import joinedload_all


class AlchemyModelManager(object):

    def __init__(self, *args, **kwargs):
        '''
        self.session is expected to be initialized
        by the derived class
        '''
        super(AlchemyModelManager, self).__init__(*args, **kwargs)

        assert hasattr(self, 'session'), "session is expected"
        assert self.session is not None, "session must be initialized" \
                                         "by the derived class"

        self.cls = self.model_class

    def list(self, filters=None):
        return self.session.query(self.cls).all()

    def retrieve(self, pk):
        query = self.session.query(self.cls)

        if hasattr(self.cls, 'navigational_fields'):
            nav_fields = '.'.join(self.cls.navigational_fields)
            query = query.options(joinedload_all(nav_fields))

        return query.get(pk)

