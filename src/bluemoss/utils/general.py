import inspect
from functools import cache
from dataclasses import fields, Field, MISSING, is_dataclass


@cache
def get_required_class_init_params(cls) -> set[str]:
    """
    :param cls: class reference
    :rtype: set[str]
    :return: The set of required initialization parameters for the given class.
    """
    return get_all_class_init_params(cls) - get_optional_class_init_params(cls)


@cache
def get_all_class_init_params(cls) -> set[str]:
    """
    :param cls: class reference
    :rtype: set[str]
    :return: The set of all initialization parameters for the given class.
    """
    return set(inspect.getfullargspec(cls.__init__).args[1:])


@cache
def get_optional_class_init_params(cls) -> set[str]:
    """
    :param cls: class reference
    :rtype: set[str]
    :return: The set of optional initialization parameters for the given class.
    """
    if is_dataclass(cls):
        return {
            f.name for f in fields(cls)
            if f.default != MISSING or f.default_factory != MISSING
        }
    return {
        name for name, param in inspect.signature(cls.__init__).parameters.items()
        if param.default != inspect.Parameter.empty
    }


__all__ = [
    "get_all_class_init_params",
    "get_optional_class_init_params",
    "get_required_class_init_params"
]
