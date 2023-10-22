import inspect
from functools import cache
from src.bluemoss.classes.utils import ClassType
from dataclasses import fields, Field, MISSING, is_dataclass


@cache
def get_class_init_params(cls: ClassType) -> set[str]:
    assert inspect.isclass(cls)
    return set(inspect.getfullargspec(cls.__init__).args[1:])


@cache
def get_class_params_with_default_value(cls: ClassType) -> set[str]:
    if is_dataclass(cls):
        return {
            f.name for f in fields(cls)
            if f.default != MISSING or f.default_factory != MISSING
        }
    return {
        name for name, param in inspect.signature(cls.__init__).parameters.items()
        if param.default != inspect.Parameter.empty
    }


def _get_default_value(f: Field) -> any:
    if f.default != MISSING:
        return f.default
    if f.default_factory != MISSING:
        return f.default_factory()


__all__ = [
    "get_class_init_params",
    "get_class_params_with_default_value"
]
