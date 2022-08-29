from dataclasses import dataclass
from enum import Enum
import time
from typing import AsyncIterable, Coroutine, Generator, Iterator
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

class STMConnector:
    def __init__(self, port, baudrate ):
        self._port = port
        self._baudrate = baudrate
        self._cachedData: dict[DataType, list[str]] = {
            DataType.DEBUG: [],
            DataType.RESPONSE: [],
            DataType.UPDATE: [],
        }
        self.receivedInfo : dict = {}
        self._receivedResponses : list = []

    async def connect(self):
        try:
            streams = await serialAsyncio.open_serial_connection(url=self._port, baudrate=self._baudrate)
            self._reader : asyncio.StreamReader = streams[0]
            self._writer : asyncio.StreamWriter = streams[1]
            self._writer.write(b'foo\n')
            await asyncio.sleep(0.5)
            await self._reader.readuntil(b'\n')
            time.sleep(.1)
            print("Connection established")
        except:
            self._reader = None
            self._writer = None
            print("Connection couldn't be established.")

    async def sendSetSensor(self): 
        return await self._sendCommand("sensor", "no")
    
    async def sendLight(self, inst): 
        return await self._sendCommand("sensor", inst)
    async def sendMotor(self, inst): 
        return await self._sendCommand("motor", inst)

    def isConnected(self):
        if(self._reader != None and self._writer != None):
            return True
        return False

    async def receiveUpdates(self) -> AsyncIterable[str]:
        while True:
            msg = await self._receiveOnly(dataType=DataType.UPDATE)
            yield msg

    async def fetchAndCacheData(self):
        while True:
            if self._currentFetching is not None:
                await self._currentFetching
                continue
            self._currentFetching = self._fetchData()
            data = await self._currentFetching
            self._cacheData(data=data)

    async def _cacheData(self, data: _Data):
        self._cachedData[data.data_type].append(data.message)

    async def _fetchData(self) -> _Data:
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

    async def _receiveOnly(self, dataType: DataType) -> str:
        while True:
            for message in self._cachedData[dataType]:
                self._cachedData[dataType].pop(0)
                return message
            if self._currentFetching is not None:
                await self._currentFetching
                continue
            self._currentFetching = self._fetchData()
            data = await self._currentFetching
            if(data.data_type == dataType):
                return data.message
            self._cachedData[data.data_type].append(data.message)

    async def getResponse(self, id):
        repeat = True
        while repeat:
            if(len(self._receivedResponses) != 0):
                repeat = False
                return 0
            await asyncio.sleep(0)

    async def _sendCommand(self, command, *argv):
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
        return self._responseStringToDic(data) 
    
    def _responseStringToDic(self, response):
        respValueList = response.split(";")
        valuesMap = {}
        for value in respValueList:
            if(value!= ""):    
                valueList = value.split("=")
                valuesMap[valueList[0]] = valueList[1]
        return valuesMap
