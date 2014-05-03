

class AlchemyModelManager(object):

    def __init__(self, *args, **kwargs):
        super(AlchemyModelManager, self).__init__(*args, **kwargs)

        assert hasattr(self, 'session'), "session is expected"
        assert self.session is not None, "session must be initialized" \
                                         "by the derived class"

        self.cls = self.model_class

    def list(self, filters=None):
        return self.session.query(self.cls).all()

    def retrieve(self, pk):
        return self.session.query(self.cls).get(pk)

