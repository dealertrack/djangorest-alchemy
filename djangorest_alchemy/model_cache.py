import importlib
import inspect
import itertools
import os

import six
from django.conf import settings


def module_walk(root_module, include_self=True):
    if isinstance(root_module, six.string_types):
        root_module = importlib.import_module(root_module)

    if include_self:
        yield root_module

    root_path = os.path.abspath(root_module.__file__)

    if '__init__' not in os.path.basename(root_path):
        return

    root_path = os.path.dirname(root_path)

    for path, dirs, files in os.walk(root_path):
        path = os.path.abspath(path)

        for file in files:
            if not file.rsplit('.', 1)[-1] == 'py':
                continue

            if file == '__init__.py':
                file = ''

            file = os.path.join(path, file)
            file = file.replace(root_path + os.sep, '')
            file = file.rsplit('.', 1)[0]

            if '.' in file:
                continue

            module_path = '.'.join(filter(
                None,
                root_module.__name__.split('.')
                + file.split(os.sep)
            ))

            module = importlib.import_module(module_path)

            yield module


class ModelCache(object):
    """
    Store for all the models in the project

    Based on Django's AppCache, this collects all the
    models in the application for introspection.

    Future:
        There will be a settings.py file which will allow
        customization
    """
    __shared_state = dict(
        modules={},
    )

    def __init__(self):
        self.__dict__ = self.__shared_state

    @property
    def models(self):
        if hasattr(self, '_models'):
            return self._models

        self._models = list(set(itertools.chain(
            *self.modules.values()
        )))

        return self._models

    def find_models_in_module(self, module_path):
        for module in module_walk(module_path, include_self=True):
            models = self._get_models_from_module(module)
            if models:
                self.modules[module.__name__] = models

    def _get_models_from_module(self, module):
        models = [
            obj for name, obj in vars(module).items()
            if (inspect.isclass(obj)
                and hasattr(obj, '_sa_class_manager'))
        ]

        return models


model_cache = ModelCache()
for path in getattr(settings, 'SA_MODEL_LOADER', []):
    model_cache.find_models_in_module(path)
