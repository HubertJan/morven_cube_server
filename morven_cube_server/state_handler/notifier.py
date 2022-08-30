from typing import Callable


class Listener:
    def __init__(self, callback: Callable[[], None]):
        self.callback = callback 

    def has_changed(self):
        self.callback()

class Notifier:
    def __init__(self):
        self._listener_to_be_notified: list[Listener] = []

    def notify(self) -> None:
        for listener in self._listener_to_be_notified:
            listener.has_changed()
    
    def add_listener(self, callback) -> Listener:
        listener = Listener(callback)
        self._listener_to_be_notified.append(listener)
        return listener