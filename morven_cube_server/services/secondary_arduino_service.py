from morven_cube_server.states.server_state import SensorData
from morven_cube_server.services.arduino_connection import ArduinoConnection, connect_to_arduino
from morven_cube_server.state_handler.notifier import Notifier

class SecondaryArduinoService(Notifier):
    def __init__(self):
        super().__init__()

    async def connect(self, port: int, baudrate: int):
        self.notify()
        self._connection = await connect_to_arduino(
            baudrate=baudrate, 
            port=port
        )
        self._port = port
        self._baudrate = baudrate

    @property
    def port(self):
        return self._port
    
    @property
    def baudrate(self):
        return self._baudrate

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