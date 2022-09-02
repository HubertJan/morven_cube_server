from dataclasses import dataclass
from morven_cube_server.models.program_settings import ArduinoConstants
from morven_cube_server.helper.cube_simulator import CubeSimulator


@dataclass(frozen=True)
class Program:
    instructions: str
    id: int
    start_pattern: str
    arduino_constants: ArduinoConstants

    @property
    def end_pattern(self) -> str:
        return CubeSimulator.simulate(self.start_pattern, instructionsString=self.instructions)

    @property
    def length(self) -> int:
        if (self.instructions == ""):
            return 0
        return self.instructions.count(" ") + 1

    @property
    def reversedProgram(self) -> list[str]:
        reversedProgram = list(self.instructions.split(" "))
        reversedProgram.reverse()
        for i, instruction in enumerate(reversedProgram):
            if len(reversedProgram[i]) == 1:
                reversedProgram[i] = reversedProgram[i][0] + "'"
            elif reversedProgram[i][1] == "'":
                reversedProgram[i] = reversedProgram[i][0]
        return reversedProgram
