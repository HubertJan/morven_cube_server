from abc import ABCMeta
from typing import Any, Optional, Type, TypeVar
from aiohttp import web


T = TypeVar("T")


def _get_application_config_data_path_by_type(type_as_string: str, ) -> str:
    return f'provider.{type_as_string}'


def provide(app: web.Application, value: T, valueType: type) -> None:
    if not isinstance(value, valueType):
        raise Exception()
    type_as_string = valueType.__name__
    path = _get_application_config_data_path_by_type(type_as_string)
    app[path] = value


def consume(app: web.Application, valueType: type[T]) -> T:
    type_as_string: str = valueType.__name__
    data: T = app[_get_application_config_data_path_by_type(type_as_string)]
    return data
