from pprint import pprint
from typing import Type, TypeVar
from morven_cube_server.zauber import run_server
from morven_cube_server.state_handler.provider import provide


def test(test: type) -> bool:
    return isinstance("test", test)


run_server()
