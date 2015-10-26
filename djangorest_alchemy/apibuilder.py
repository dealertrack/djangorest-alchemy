"""
API Builder
Build dynamic API based on the provided SQLAlchemy model
"""
from .managers import AlchemyModelManager
from .routers import ReadOnlyRouter
from .viewsets import AlchemyModelViewSet


class APIModelBuilder(object):
    def __init__(self,
                 models,
                 base_managers,
                 base_viewsets=None,
                 *args, **kwargs):
        self.models = models

        if not isinstance(base_managers, (tuple, list)):
            base_managers = [base_managers]
        if not isinstance(base_managers, tuple):
            base_managers = tuple(base_managers)
        if base_viewsets is None:
            base_viewsets = (AlchemyModelViewSet,)

        self.base_managers = base_managers
        self.base_viewsets = base_viewsets

    @property
    def urls(self):
        router = ReadOnlyRouter()

        for model in self.models:
            manager = type(
                str('{}Manager'.format(model.__name__)),
                self.base_managers + (AlchemyModelManager,),
                {
                    'model_class': model,
                }
            )
            viewset = type(
                str('{}ModelViewSet'.format(model.__name__)),
                self.base_viewsets,
                {
                    'manager_class': manager,
                    'paginate_by': 10,
                }
            )

            router.register('data-api/' + model.__name__.lower() + 's',
                            viewset,
                            base_name=model.__name__)

        return router.urls
