'''
Base for interfacing with SQLAlchemy
Provides the necessary plumbing for CRUD
using SA session
'''
from inspector import class_keys, primary_key


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
        '''
        List returns back list of URI
        In case of multiple pks, We guess the pk
        by using '<modelname>_id' as the field convention
        '''
        pk = primary_key(self.cls)

        queryset = self.session.query(self.cls.__dict__[pk]).all()

        newlist = list()
        for pk_val in queryset:
            cls_inst = self.cls()
            setattr(cls_inst, pk, pk_val[0])
            newlist.append(cls_inst)

        return newlist

    def retrieve(self, pks):

        newargs = list(pks)
        for key in class_keys(self.cls):
            if key in self.context:
                newargs.append(self.context[key])

        return self.session.query(self.cls).get(newargs)

