from morven_cube_server.services.arduino_connection import ArduinoConnection, ArduinoService


class PrimaryArduinoService:
    def __init__(self, connection: ArduinoConnection):
        self._connection = connection

    async def sendProgram(self, instructions: str, programId, isDouble = True, acc50 = 42000, acc100=43000, cc50=19, cc100=20, maxSp=4000): #replace current program
        doubleStr =  "1" if isDouble else "0"
        return await self._connection.send_command("program", instructions, programId, doubleStr, str(acc50), str(acc100), str(cc50), str(cc100), str(maxSp))

    async def sendPrepareAndProgram(self, instructions: str, programId, prepareInstructions): #replace current program
        return await self._connection.send_command("program", instructions, programId, prepareInstructions)

    async def send_status(self, newStatus):
        if(newStatus == "PAUSE"):
            await self.connection.send_command("pause true")
        elif(newStatus == "RUN" ):
            await self.connection.send_command("pause false")

    async def handle_received_updates(self):
        while True:
            data = await self._connection.fetch_updates()
            sensor_data: SensorData = convert_to_sensor_data(data)
             if (data.__contains__("id")):
                if(self._currentProgram == None or (self._currentProgram != None and self._currentProgram.id != data["id"])):
                    self._currentProgram = Program(
                        data["in"], data["id"], self._cubePattern.pattern)
                    self._currentInstructionId = data["ci"]
                    self._programRunningTime = int(data["rt"])
                if (data.__contains__("li")):
                    self._cubePattern.imposeInstructions(
                        data["li"])
                if (data.__contains__("st")):
                    self._status = data["st"]
                if(self._status == "FINISHED"):
                    self._saveCurrentProgramAsRecord()
                self._mainArduinoConnection.receivedInfo.clear()