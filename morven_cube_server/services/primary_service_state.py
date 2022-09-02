from typing import AsyncGenerator, AsyncIterator, Awaitable
from morven_cube_server.models.end_of_program_report import EndOfProgramReport
from morven_cube_server.models.program import Program
from morven_cube_server.models.running_program_report import RunningProgramReport
from morven_cube_server.services.primary_service import PrimaryService
from morven_cube_server.states.server_state import SensorData
from morven_cube_server.services.api.arduino_connection import ArduinoConnection
from morven_cube_server.state_handler.notifier import Notifier


class PrimaryArduinoService(Notifier):
    def __init__(self, connection: ArduinoConnection):
        self._connection = connection

    # replace current program
    async def send_program(self, program: Program) -> None:
        await self._connection.send_command(
            "program",
            program.instructions,
            program.id,
            program.arduino_constants.is_double,
            program.arduino_constants.acc50,
            program.arduino_constants.acc100,
            program.arduino_constants.cc50,
            program.arduino_constants.cc100,
            program.arduino_constants.max_speed
        )
        return None

    async def pause(self) -> None:
        await self._connection.send_command("pause true")
        return None

    async def unpause(self) -> None:
        await self._connection.send_command("pause false")
        return None

    async def handle_received_updates(self) -> AsyncIterator[EndOfProgramReport | RunningProgramReport]:
        while True:
            data = await self._connection.fetch_updates()
            #sensor_data: SensorData = convert_to_sensor_data(data)
            yield data  # : SensorData
