"""
API Builder
Build dynamic API based on the provided SQLAlchemy model
"""
from viewsets import AlchemyModelViewSet
from rest_framework_nested import routers
from managers import AlchemyModelManager


class APIModelBuilder(object):

    def __init__(self, models, SessionMixin, *args, **kwargs):
        self.models = models
        self.SessionMixin = SessionMixin

    @property
    def urls(self):
        router = routers.SimpleRouter()

        for model in self.models:

            manager = type(
                str('{}Manager'.format(model.__name__)),
                (self.SessionMixin, AlchemyModelManager,),
                {
                    'model_class': model,
                }
            )
            viewset = type(
                str('{}ModelViewSet'.format(model.__name__)),
                (AlchemyModelViewSet,),
                {
                    'manager_class': manager,
                }
            )

            router.register('data-api/' + model.__name__.lower() + 's', viewset,
                            base_name=model.__name__)

        return router.urls
