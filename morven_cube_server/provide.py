from typing import Any, Optional, Type, TypeVar
from aiohttp import web

T = TypeVar("T")

def _get_application_config_data_path_by_type(type_as_string: str, ) -> str:
    return f'provider.{type_as_string}'

def provide(app: web.Application, value: T, valueType: Type[T]) -> None:
    type_as_string = valueType.__name__
    app[_get_application_config_data_path_by_type(type_as_string)] = value

def consume(app: web.Application, valueType: Type[T]) -> T:
    type_as_string = valueType.__name__
    return app[_get_application_config_data_path_by_type(type_as_string)]

