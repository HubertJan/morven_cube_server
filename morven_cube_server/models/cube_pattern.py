from __future__ import annotations

from morven_cube_server.helper.cube_simulator import CubeSimulator
from morven_cube_server.helper.kociemba_extend import Kociemba as kociemba


class CubePattern:
    def __init__(self, patttern: str):
        self._pattern = patttern

    def execute_instructions(self, instructions: str) -> CubePattern:
        calculated_pattern = CubeSimulator.simulate(
            self._pattern, instructions)
        return CubePattern(calculated_pattern)

    def __str__(self) -> str:
        return self._pattern
