from typing import AsyncGenerator, AsyncIterator, Awaitable
from morven_cube_server.models.end_of_program_report import EndOfProgramReport
from morven_cube_server.models.program import Program
from morven_cube_server.models.running_program_report import RunningProgramReport
from morven_cube_server.services.primary_service import PrimaryService
from morven_cube_server.states.server_state import SensorData
from morven_cube_server.services.api.arduino_connection import ArduinoConnection, connect_to_arduino
from morven_cube_server.state_handler.notifier import Notifier


class PrimaryArduinoService(Notifier):
    async def connect(self, port: str, baudrate: int):
        self._connection = await connect_to_arduino(port, baudrate)

    # replace current program
    async def send_program(self, program: Program) -> None:
        await self._connection.send_command(
            "program",
            program.instructions,
            program.id,
            "1" if program.arduino_constants.is_double else "0",
            str(program.arduino_constants.acc50),
            str(program.arduino_constants.acc100),
            str(program.arduino_constants.cc50),
            str(program.arduino_constants.cc100),
            str(program.arduino_constants.max_speed)
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
            raw_data = await self._connection.fetch_updates()
            #sensor_data: SensorData = convert_to_sensor_data(data)
            data = _response_string_to_dic(raw_data)
            if(data["st"] == "FINISHED"):
                data = convert_response_dict_to_end_of_program_report(data)
                yield data  # : SensorData


def convert_response_dict_to_end_of_program_report(data_dict) -> EndOfProgramReport:
    return EndOfProgramReport(
        program_id=data_dict["id"],
        instructions=data_dict["in"],
        runtime=data_dict["rt"]
    )


def _response_string_to_dic(response: str) -> dict[str, any]:
    respValueList = response.split(";")
    valuesMap = {}
    for value in respValueList:
        if (value != ""):
            valueList = value.split("=")
            valuesMap[valueList[0]] = valueList[1]
    return valuesMap
