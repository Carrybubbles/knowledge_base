# -*- coding: utf-8 -*-
import os
import importlib

module_path = os.path.dirname(os.path.abspath(__file__))
apis = [f for f in os.listdir(module_path) if f.endswith(".py") and f != "__init__.py"]
__all__ = apis
for api in apis:
    importlib.import_module("web.apis.%s" % api[:-3])

print(
    "Imported views: %s" % ", ".join(apis)
    if apis
    else "No views avaiable in the views directory."
)

