from dataclasses import dataclass
from enum import Enum
import time
from typing import Any, Coroutine
import serial
import serial_asyncio as serialAsyncio
import asyncio

class DataType(Enum):
    UPDATE= 0
    RESPONSE= 1
    DEBUG= 2

@dataclass
class _Data:
    data_type: DataType
    message: str

class ArduinoConnection:
    def __init__(self, reader : asyncio.StreamReader, writer : asyncio.StreamWriter,):
        self._writer = writer
        self._reader = reader
        self._current_fetching : Coroutine[Any, Any, _Data] | None = None
        self._cached_data: dict[DataType, list[str]] = {
            DataType.DEBUG: [],
            DataType.RESPONSE: [],
            DataType.UPDATE: [],
        }

    async def fetch_updates(self) -> str:
        return await self._fetch_only_and_cache_rest(DataType.UPDATE)

    async def fetch_reponse(self) -> str:
        return await self._fetch_only_and_cache_rest(DataType.RESPONSE)

    async def fetch_debug(self) -> str:
        return await self._fetch_only_and_cache_rest(DataType.DEBUG)

    # returns latest unhandled data in cache of [data_type]
    # if no unhandled data exist, it fetches new data
    # if other func already fetches data, it waits until other func is done
    async def _fetch_only_and_cache_rest(self, data_type: DataType) -> str:
        while True:
            data_from_cache = self._handle_data_from_cache(data_type)
            if data_from_cache is not None:
                return data_from_cache
            if self._current_fetching is not None:
                await self._current_fetching
                continue
            self._current_fetching = self._fetch_data()
            fetched_data: _Data = await self._current_fetching
            if fetched_data.data_type != data_type:
                self._cache(fetched_data)
                continue
            return fetched_data.message
            
    def _cache(self, data: _Data):
        self._cached_data[data.data_type].append(data.message)

    def _handle_data_from_cache(self, dataType: DataType):
        if len(self._cached_data[dataType]) == 0:
            return None
        msg = self._cached_data[dataType].pop(0)
        return msg

    async def _fetch_data(self) -> _Data:
        rawData = await self._reader.readuntil(b'\n')
        dataString = str(rawData)
        data = dataString[2:len(dataString)-5]
        data_sender_list =  data.split(";", 1)
        channel = data_sender_list[0]
        message = data_sender_list[1]
        if(channel == "debug"):
            return _Data(data_type=DataType.DEBUG, message=message)            
        elif(channel == "response"):
            return _Data(data_type=DataType.RESPONSE, message=message)      
        elif(channel == "data"):
            return _Data(data_type=DataType.UPDATE, message=message)      
        raise Exception("Invalid channel")
    
    async def send_command(self, command, *argv):
        commandString = command
        for arg in argv:
            commandString = commandString + ' "'  + arg + '"'
        commandString = commandString + "\n"
        print("Command:" + commandString)
        self._writer.write(commandString.encode())
        responseId = await self.getResponse("TEST")
        data = self._receivedResponses.pop(responseId)
        if (data == ""):
            return
        return self._response_string_to_dic(data) 
    
    def _response_string_to_dic(self, response):
        respValueList = response.split(";")
        valuesMap = {}
        for value in respValueList:
            if(value!= ""):    
                valueList = value.split("=")
                valuesMap[valueList[0]] = valueList[1]
        return valuesMap


async def connect_to_arduino(port: int, baudrate: int) -> ArduinoConnection:
    try:
        streams = await serialAsyncio.open_serial_connection(url=port, baudrate=baudrate)
        reader : asyncio.StreamReader = streams[0]
        writer : asyncio.StreamWriter = streams[1]
        writer.write(b'foo\n')
        await asyncio.sleep(0.5)
        await reader.readuntil(b'\n')
        time.sleep(.1)
        return ArduinoConnection(reader=reader, writer=writer)
    except:
        raise Exception("Can not connect to Arduino.")