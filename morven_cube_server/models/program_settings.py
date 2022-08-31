from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ArduinoConstants:
    acc50: int
    acc100: int
    cc50: int
    cc100: int
    max_speed: int
    is_double: bool

    def update(self, acc50: Optional[int] = None, acc100: Optional[int] = None, cc50: Optional[int] = None, cc100: Optional[int] = None, max_speed: Optional[int] = None, is_double: Optional[bool] = None) -> ArduinoConstants:
        return ArduinoConstants(
            acc50=acc50 if acc50 is not None else self.acc50,
            acc100=acc100 if acc100 is not None else self.acc100,
            cc50=cc50 if cc50 is not None else self.acc50,
            cc100=cc100 if cc100 is not None else self.cc100,
            is_double=is_double if is_double is not None else self.is_double,
            max_speed=max_speed if max_speed is not None else self.max_speed
        )
