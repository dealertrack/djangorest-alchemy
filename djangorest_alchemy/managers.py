'''
Base for interfacing with SQLAlchemy
Provides the necessary plumbing for CRUD
using SA session
'''
from inspector import class_keys, primary_key, KeyNotFoundException


class AlchemyModelManager(object):

    def __init__(self, *args, **kwargs):
        '''
        self.session is expected to be initialized
        by the derived class
        '''
        self.cls = self.model_class

        #Throws error in tests
        #super(AlchemyModelManager, self).__init__(*args, **kwargs)

        assert hasattr(self, 'session'), "session is expected"
        assert self.session is not None, "session must be initialized" \
                                         "by the derived class"

    def list(self, other_pks=None, filters=None):
        '''
        List returns back list of URI
        In case of multiple pks, We guess the pk
        by using '<modelname>_id' as the field convention
        '''
        newlist = list()
        try:
            pk = primary_key(self.cls)
        except KeyNotFoundException:
            return newlist

        filter_dict = dict()

        if filters:
            filter_dict = {k:v for k, v in filters.iteritems()}

        if other_pks:
            other_pks.update(filter_dict)
            queryset = self.session.query(self.cls.__dict__[pk]).filter_by(**other_pks).all()
        else:
            if filter_dict:
                queryset = self.session.query(self.cls.__dict__[pk]).filter_by(**filter_dict).all()
            else:
                queryset = self.session.query(self.cls.__dict__[pk]).all()

        for pk_val in queryset:
            cls_inst = self.cls()
            setattr(cls_inst, pk, pk_val[0])
            newlist.append(cls_inst)

        return newlist

    def retrieve(self, pks, other_pks=None):
        '''
        Retrieve fetches the object based on the following pk logic:
        if 'other' pks are not found, just use the pk list (coming from URLS)
        assuming their order is already correct
        if 'other' pks are found, then use the class keys to
        get the correct order of pks, look them up
        '''

        if not other_pks:
            newargs = list(pks)
        else:
            newargs = list()
            pk_added = False
            for key in class_keys(self.cls):
                if other_pks and key in other_pks:
                    newargs.append(other_pks[key])
                else:
                    if not pk_added:
                        newargs.append(pks[-1])
                        pk_added = True

            # Confirm this logic works!!!
            # will the order be correct if we just append?
            for pk in pks[:-1]:
                newargs.append(pk)

        return self.session.query(self.cls).get(newargs)

