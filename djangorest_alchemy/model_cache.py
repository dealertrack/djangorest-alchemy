import importlib
import inspect
import itertools
import os


class ModelCache(object):
    """Store for all the models in the project

    Based on Django's AppCache, this collects all the
    models in the application for introspection.

    Future:
        There will be a settings.py file which will allow
        customization
    """
    __shared_state = dict(
        modules={},
        models=[]
    )

    def __init__(self):
        self.__dict__ = self.__shared_state

    def get_module_names_and_path(self, directory_path="."):
        all_paths = []

        for root, dirs, files in os.walk(directory_path):
            all_paths.extend(
                [(file[:-3], os.path.join(root, file))
                 for file in files if
                 file.endswith(".py") and file.startswith("models")]
            )

        return all_paths

    def get_models_from_modules(self, module_name):
        module = importlib.import_module(module_name)

        models = [
            obj for name, obj in vars(module).items()
            if (inspect.isclass(obj)
                and hasattr(obj, '__tablename__'))
        ]

        return models


model_cache = ModelCache()
model_cache.modules = {
    module[0]: module[1]
    for module in model_cache.get_module_names_and_path()
}

model_cache.models = list(itertools.chain(*[
    model_cache.get_models_from_modules(module)
    for module in model_cache.modules.keys()
]))
