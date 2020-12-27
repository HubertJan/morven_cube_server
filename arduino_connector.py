import time
import serial
import serial_asyncio as serialAsyncio
import asyncio

class ArduinoConnection:
    def __init__(self, port, baudrate ):
        self._port = port
        self._baudrate = baudrate
        self.receivedInfo : dict = {}
        self._receivedResponses : list = []

    async def connect(self):
        try:
            self._reader, self._writer = await serialAsyncio.open_serial_connection(url='/COM3', baudrate=9600)
            await self._reader.readuntil(b'\n')
            time.sleep(.1)
            print("Connection established")
        except:
            self._reader = None
            self._writer = None
            print("Connection couldn't be established.")

    async def sendProgram(self, instructions: str, programId): #replace current program
        return await self._sendCommand("program", instructions, programId )
    async def sendPrepareAndProgram(self, instructions: str, programId, prepareInstructions): #replace current program
        return await self._sendCommand("program", instructions, programId, prepareInstructions)
    
    async def sendInstructions(self, instruction): #add Instruction to program
        await self._sendCommand("")
        
    def isConnected(self):
        if(self._reader != None and self._writer != None):
            return True
        return False
    
    def sendStatus(self, newStatus):
        if(newStatus == "working"):
            self._sendCommand("continue")
        elif(newStatus == "paused" ):
            self._sendCommand("pause")
    
    async def loopReceivingData(self):
        while True:
            await self._receiveData()
        
    async def _receiveData(self):
        rawData = await self._reader.readuntil(b'\n')
        dataString = str(rawData)
        data = dataString[2:len(dataString)-5]
        dataSenderList =  data.split(";", 1)
        sender = dataSenderList[0]
        if(sender == "debug"):
            print (dataSenderList[1])
        elif(sender == "response"):
            self._receivedResponses.append(dataSenderList[1])
        elif(sender == "data"):
            self.receivedInfo.update(self._responseStringToDic(dataSenderList[1]))


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
