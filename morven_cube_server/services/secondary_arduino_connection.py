from dataclasses import dataclass
from typing import Optional

from morven_cube_server.services.arduino_connection import ArduinoConnection

@dataclass
class SensorData:
    temp1: Optional[int]
    temp2: Optional[int]
    temp3: Optional[int]
    volt1: Optional[int]
    volt2: Optional[int]
    volt3: Optional[int]

class SecondaryArduinoService:
    def __init__(self, connection: ArduinoConnection):
        self._connection = connection

    async def sendSetSensor(self): 
        return await self._connection.send_command("sensor", "no")
    
    async def sendLight(self, inst): 
        return await self._connection.send_command("sensor", inst)

    async def sendMotor(self, inst): 
        return await self._connection.send_command("motor", inst)

    async def handle_received_sensor_data(self):
        while True:
            data = await self._connection.fetch_updates()
            sensor_data: SensorData = convert_to_sensor_data(data)
            if (data.__contains__("t1")):
                    self._sensorData["temp1"] = data["t1"]
            if (data.__contains__("t2")):
                self._sensorData["temp2"] = data["t2"]
            if (data.__contains__("t3")):
                self._sensorData["temp3"] = data["t3"]
            if (data.__contains__("v1")):
                self._sensorData["volt1"] = data["v1"]
            if (data.__contains__("v2")):
                self._sensorData["volt2"] = data["v2"]
            if (data.__contains__("v3")):
                self._sensorData["volt3"] = data["v3"]
            yield sensor_data