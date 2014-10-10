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

        assert hasattr(self, 'session'), "session is expected"
        assert self.session is not None, "session must be initialized" \
                                         "by the derived class"

    def list(self, other_pks=None, filters=None):
        '''
        List returns back list of URI
        In case of multiple pks, We guess the pk
        by using '<modelname>_id' as the field convention
        '''
        try:
            pk = primary_key(self.cls)
        except KeyNotFoundException:
            pk = None

        filter_dict = dict()

        if filters:
            filter_dict = {k: v for k, v in filters.iteritems()}
            filter_dict.pop('format', None)
            filter_dict.pop('page', None)
            filter_dict.pop('sort_by', None)

        if other_pks:
            query_pks = dict()

            # Use only those keys which are primary keys
            # and pick them up from the passed dict
            for key in class_keys(self.cls):
                if key in other_pks:
                    query_pks[key] = other_pks[key]

            query_pks.update(filter_dict)

            if pk:
                queryset = self.session.query(self.cls.__dict__[pk]).filter_by(
                    **query_pks).all()
            else:
                queryset = self.session.query(self.cls).filter_by(
                    **query_pks).all()
        else:
            if filter_dict:
                if pk:
                    queryset = self.session.query(
                        self.cls.__dict__[pk]).filter_by(
                        **filter_dict).all()
                else:
                    queryset = self.session.query(self.cls).filter_by(
                        **filter_dict).all()
            else:
                if pk:
                    queryset = self.session.query(self.cls.__dict__[pk]).all()
                else:
                    # Limit to 1000 rows, this is worst case scenario
                    queryset = self.session.query(self.cls).limit(1000).all()

        return queryset

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
            for key in class_keys(self.cls):
                if other_pks and key in other_pks:
                    newargs.append(other_pks[key])

            # Confirm this logic works!!!
            # will the order be correct if we just append?
            for pk in reversed(pks):
                newargs.append(pk)

        return self.session.query(self.cls).get(newargs)
