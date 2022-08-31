from typing import Any, AsyncIterator
import typing
from morven_cube_server.states.server_state import SensorData
from morven_cube_server.services.arduino_connection import ArduinoConnection, connect_to_arduino
from morven_cube_server.state_handler.notifier import Notifier


class SecondaryArduinoService(Notifier):
    async def connect(self, port: int, baudrate: int) -> None:
        self.notify()
        self._connection = await connect_to_arduino(
            baudrate=baudrate,
            port=port
        )
        self._port = port
        self._baudrate = baudrate

    @property
    def port(self) -> int:
        return self._port

    @property
    def baudrate(self) -> int:
        return self._baudrate

    async def send_light(self, inst: str) -> None:
        await self._connection.send_command("sensor", inst)

    async def sendMotor(self, inst: str) -> None:
        await self._connection.send_command("motor", inst)

    async def handle_received_sensor_data(self) -> AsyncIterator[SensorData]:
        while True:
            data: dict[str, Any] = await self._connection.fetch_updates()
            sensor_data: SensorData = _convert_to_sensor_data(data)
            yield sensor_data


def _convert_to_sensor_data(data: dict[str, typing.Any]) -> SensorData:
    sensor_data = SensorData()
    if (data.__contains__("t1")):
        sensor_data = sensor_data.update(
            temp1=int(data["t1"])
        )
    if (data.__contains__("t2")):
        sensor_data = sensor_data.update(
            temp2=int(data["t2"])
        )
    if (data.__contains__("t3")):
        sensor_data = sensor_data.update(
            temp3=int(data["t3"])
        )
    if (data.__contains__("v1")):
        sensor_data = sensor_data.update(
            volt1=int(data["v1"])
        )
    if (data.__contains__("v2")):
        sensor_data = sensor_data.update(
            volt2=(data["v1"])
        )
    if (data.__contains__("v3")):
        sensor_data = sensor_data.update(
            volt3=int(data["v1"])
        )
    return sensor_data
