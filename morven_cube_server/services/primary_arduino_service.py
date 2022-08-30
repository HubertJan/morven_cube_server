from typing import AsyncGenerator
from morven_cube_server.models.server_state import SensorData
from morven_cube_server.services.arduino_connection import ArduinoConnection, ArduinoService



class PrimaryArduinoService:
    def __init__(self, connection: ArduinoConnection):
        self._connection = connection

    async def send_program(self, instructions: str, programId, isDouble = True, acc50 = 42000, acc100=43000, cc50=19, cc100=20, maxSp=4000): #replace current program
        doubleStr =  "1" if isDouble else "0"
        return await self._connection.send_command("program", instructions, programId, doubleStr, str(acc50), str(acc100), str(cc50), str(cc100), str(maxSp))

    async def sendPrepareAndProgram(self, instructions: str, programId, prepareInstructions): #replace current program
        return await self._connection.send_command("program", instructions, programId, prepareInstructions)

    async def send_status(self, newStatus):
        if(newStatus == "PAUSE"):
            await self.connection.send_command("pause true")
        elif(newStatus == "RUN" ):
            await self.connection.send_command("pause false")

    async def handle_received_updates(self) -> AsyncGenerator[SensorData, None]:
        while True:
            data = await self._connection.fetch_updates()
            sensor_data: SensorData = convert_to_sensor_data(data)
            yield sensor_data