from typing import Callable, Protocol, Any


""""
do()
Used for lambda func, that are not supposed to return anything
e.g. foo(e: Callable[[], None]) bar(arg: str) -> str
foo(lambda: bar("cat")) wouldn't work, because bar returns str
foo(lambda: do(bar("cat")) works, because do return None
"""


def do(_: Any) -> None:
    pass


class Listener:
    def __init__(self, callback: Callable[[], None]):
        self.callback = callback

    def has_changed(self) -> None:
        self.callback()


class SupportsAddListener(Protocol):
    def add_listener(self, callback: Callable[[], None]) -> Listener:
        pass


class Notifier:
    def __init__(self) -> None:
        self._listener_to_be_notified: list[Listener] = []

    def notify(self) -> None:
        for listener in self._listener_to_be_notified:
            listener.has_changed()

    def add_listener(self, callback: Callable[[], None]) -> Listener:
        listener = Listener(callback)
        self._listener_to_be_notified.append(listener)
        return listener
