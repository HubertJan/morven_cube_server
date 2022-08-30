from typing import AsyncGenerator
from morven_cube_server.models.end_of_program_report import EndOfProgramReport
from morven_cube_server.models.program import Program
from morven_cube_server.models.running_program_report import RunningProgramReport
from morven_cube_server.states.server_state import SensorData
from morven_cube_server.services.arduino_connection import ArduinoConnection, ArduinoService

class PrimaryArduinoService:
    def __init__(self, connection: ArduinoConnection):
        self._connection = connection

    async def send_program(self, program: Program): #replace current program
        return await self._connection.send_command(
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

    async def pause(self):
        await self.connection.send_command("pause true")

    async def unpause(self):
        await self.connection.send_command("pause false")

    async def handle_received_updates(self) -> AsyncGenerator[EndOfProgramReport | RunningProgramReport, None]:
        while True:
            data = await self._connection.fetch_updates()
            #sensor_data: SensorData = convert_to_sensor_data(data)
            yield data #: SensorData
    
