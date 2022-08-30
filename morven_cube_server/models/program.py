from dataclasses import dataclass
from morven_cube_server.models.program_settings import ArduinoConstants


@dataclass(frozen=True)
class Program:
    instructions: str
    id: str
    start_pattern: str
    end_pattern: str
    arduino_constants: ArduinoConstants

    @property
    def length(self):
        if (self._instructions == ""):
            return 0
        return self._instructions.count(" ") + 1

    @property
    def reversedProgram(self):
        reversedProgram = list(self._instructions.split(" "))
        reversedProgram.reverse()
        for i, instruction in enumerate(reversedProgram):
            if len(reversedProgram[i]) == 1:
                reversedProgram[i] = reversedProgram[i][0] + "'"
            elif reversedProgram[i][1] == "'":
                reversedProgram[i] = reversedProgram[i][0]
        return reversedProgram
