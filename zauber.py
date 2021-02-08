import uuid
import asyncio
import time
from aiohttp import web
from datetime import datetime
from enum import Enum

import numpy as np

from helper.kociemba_extend import Kociemba as kociemba
from database import RubiksDatabase
from arduino_connector import ArduinoConnection
from stm_connector import STMConnector
from classes.cube_pattern import CubePattern
from helper.cubeSimulator import CubeSimulator
from classes.program import Program
from classes.program_pointer import ProgramPointer
from helper.stoppWatch import StoppWatch


class Zauber:
    def __init__(self, ):
        try:
            self._db = RubiksDatabase("/db_cube.csv")
            self._mainArduinoConnection = ArduinoConnection("/COM3", 9600)
            self._secondaryArduinoConnection = STMConnector("/COM4", 9600)
            self._cubePattern = None
            self._currentProgram: Program = None
            self._status = "NOT FETCHED"
            self._currentInstructionId = None
            self._programRunningTime = 0
            self._server = web.Application()
            self._sensorData = {
                "temp1" : 0,
                "temp2" : 0,
                "temp3" : 0,
                "volt1" : 0,
                "volt2" : 0,
                "volt3" : 0,
            }
            self._routes = [
                web.get("/status", self.handlerGetStatus),
                web.patch("/status/{arguments}", self.handlerPatchStatus),
                web.get("/program", self.handlerGetProgram),
                web.post("/program/{arguments}", self.handlerPostProgram),
                web.get("/pattern", self.handlerGetPattern),
                web.post("/pattern/{arguments}", self.handlerPostPattern),
                web.get("/process", self.handlerGetProcess),
                web.get("/records", self.handlerGetRecords),
                web.get("/sensor", self.handlerGetSensor)
            ]
        except:
            return

    @property
    def _futureCubePattern(self):
        self._secondaryArduinoConnection.sendLight("BL")
        self._secondaryArduinoConnection.sendLight("WH")
        self._secondaryArduinoConnection.sendMotor("OP")
        self._secondaryArduinoConnection.sendLight("BL")
        self._secondaryArduinoConnection.sendLight("WH")
        self._secondaryArduinoConnection.sendMotor("CL")
        return self._cubePattern.pattern

    async def handlerGetStatus(self, request):
        resp = web.json_response(
            {
                "status": self._status,
                "programId": self._currentProgram.id if self._currentProgram.id != None else "",
                "currentPattern": self._cubePattern.pattern,
            },
            status=200
        )
        return resp

    async def handlerGetProcess(self, request):
        resp = web.json_response(
            {
                "status": self._status,
                "program":  self._currentProgram.instructions if self._currentProgram.instructions != None else "",
                "programId": self._currentProgram.id if self._currentProgram.id != None else "",
                "currentInstructionId": self._currentInstructionId if self._currentInstructionId != None else "",
                "startPattern": self._currentProgram.startPattern,
                "endPattern": self._currentProgram.endPattern,
                "time": self._programRunningTime,
            },
            status=200
        )
        return resp

    async def handlerGetSensor(self, request):
        resp = web.json_response(
            {
                "temp": self._sensorData["temp1"],
                "temp2": self._sensorData["temp2"],
                "c2": 4
            },
            status=200
        )
        return resp

    async def handlerPatchStatus(self, request):
        command = request.rel_url.name
        if command != "RUN" or command != "PAUSE":
            return web.json_response(
                status=403
            )
        await self._mainArduinoConnection.sendStatus(command)
        resp = web.json_response(
            {
                "status": self._status,
            },
            status=200
        )
        return resp

    async def handlerGetProgram(self, request):
        if self._currentProgram == None:
            resp = web.json_response(
                {
                    "currentProgram": None,
                },
                status=200
            )

        else:
            resp = web.json_response(
                {
                    "currentProgram": self._currentProgram.instructions,
                    "currentProgramId": self._currentProgram.id,
                    "currentInstructionId": self._currentInstructionId,
                },
                status=200
            )
        return resp

    async def handlerPostProgram(self, request):
        if(self._status == "RUN"):
            return web.json_response(
                {
                    "msg": "A program is already running."
                },
                status=403)

        inst = request.rel_url.name
        return await self._createAndSendProgramByInstructions(inst)

    async def handlerGetPattern(self, request):
        resp = web.json_response(
            {
                "currentPattern": self._cubePattern.pattern,
                "futurePattern": self._futureCubePattern,
            },
            status=200
        )
        return resp

    def getOptionalArguemnts(self, optionalArguments: dict, data):
        for key in optionalArguments.keys():
            if key in data:
                optionalArguments[key] = data[key]

        return optionalArguments

    async def handlerPostPattern(self, request):
        if(self._status == "RUN"):
            return web.json_response(
                {
                    "msg": "A program is already running."
                },
                status=403)

        optionalArguments = {
            "isDouble": True,
            "acc50": 42000,
            "acc100": 4300,
            "cc50": 19,
            "cc100": 20,
            "maxSp": 4000,
        }

        optionalArguments = self.getOptionalArguemnts(
            optionalArguments, request.rel_url.query)

        command = request.rel_url.name

        if(command == "solve" or command == ""):
            inst = kociemba.solve(self._cubePattern.pattern)
            resp = await self._createAndSendProgramByInstructions(inst, isDouble=optionalArguments["isDouble"], acc50=optionalArguments["acc50"], acc100=optionalArguments["acc100"], cc50=optionalArguments["cc50"], cc100=optionalArguments["cc100"], maxSp=optionalArguments["maxSp"])
        elif(command == "scramble"):
            inst = CubeSimulator.getScramble()
            resp = await self._createAndSendProgramByInstructions(inst, isDouble=optionalArguments["isDouble"], acc50=optionalArguments["acc50"], acc100=optionalArguments["acc100"], cc50=optionalArguments["cc50"], cc100=optionalArguments["cc100"], maxSp=optionalArguments["maxSp"])
        else:
            pattern = command
            resp = await self._createAndSendProgramByPattern(pattern, isDouble=optionalArguments["isDouble"], acc50=optionalArguments["acc50"], acc100=optionalArguments["acc100"], cc50=optionalArguments["cc50"], cc100=optionalArguments["cc100"], maxSp=optionalArguments["maxSp"])
        return resp

    async def handlerGetRecords(self, request):
        resp = web.json_response(
            {
                "records": self._db.records,
            },
            status=200
        )
        return resp

    async def _createAndSendProgramByInstructions(self, instructions: str, isDouble=True, acc50=42000, acc100=43000, cc50=19, cc100=20, maxSp=4000):
        if(CubeSimulator.validCheckOfInstructions(instructions) == False):
            return web.json_response(
                {
                    "msg": "Invalid instructions",
                },
                status=400
            )
        programId = uuid.uuid4().hex
        programData = await self._mainArduinoConnection.sendProgram(instructions, programId, isDouble=isDouble, acc50=acc50, acc100=acc100, cc50=cc50, cc100=cc100, maxSp=maxSp)
        self._currentProgram = Program(
            programData["programInstructions"], programData["programId"], self._cubePattern.pattern)
        self._currentInstructionId = 0
        self._status = "RUN"
        self._programRunningTime = 0
        return web.json_response(
            {
                "currentProgram": self._currentProgram.instructions,
                "currentProgramId": self._currentProgram.id,
                "currentProgramLength": self._currentProgram.length,
                "currentInstructionId": self._currentInstructionId,
            },
            status=200
        )

    async def _createAndSendProgramByPattern(self, pattern: str, isDouble=True, acc50=42000, acc100=43000, cc50=19, cc100=20, maxSp=4000):
        if(CubeSimulator.validCheckOfPattern(pattern)):
            inst = kociemba.solve(self._cubePattern.pattern, pattern)
            return await self._createAndSendProgramByInstructions(inst,  isDouble=isDouble, acc50=acc50, acc100=acc100, cc50=cc50, cc100=cc100, maxSp=maxSp)
        else:
            return web.json_response(
                {
                    "msg": "Invalid pattern",
                },
                status=400
            )

    def _getCamData(self):
        self._secondaryArduinoConnection.
        time.sleep(5)
        return 'DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD'

    def _saveCurrentProgramAsRecord(self):
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        self._db.addRecord(self._currentProgram.id,
                           self._currentProgram.startPattern,
                           self._currentProgram.endPattern,
                           self._currentProgram.instructions,
                           self._programRunningTime,
                           date_time,
                           )

    async def _handleReceivedData(self):
        while True:
            if(len(self._mainArduinoConnection.receivedInfo) == 0):
                await asyncio.sleep(0)
            else:
                data: dict = self._mainArduinoConnection.receivedInfo
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

    async def _handleReceivedDataSecondary(self):
        while True:
            if(len(self._secondaryArduinoConnection.receivedInfo) == 0):
                await asyncio.sleep(0)
            else:
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
                data: dict = self._secondaryArduinoConnection.receivedInfo
                self._secondaryArduinoConnection.receivedInfo.clear()
    
    async def setupSecondary(self):
        self._secondaryArduinoConnection.sendSetSensor()
        self._cubePattern = CubePattern(self._getCamData())

    async def runService(self):
        await self._mainArduinoConnection.connect()
       # await self._secondaryArduinoConnection.connect()
        if(self._mainArduinoConnection.isConnected() and self._secondaryArduinoConnection.isConnected):
            self._server.router.add_routes(self._routes)
            await asyncio.gather(
                web._run_app(self._server,  host='localhost', port=9000),
                self._mainArduinoConnection.loopReceivingData(),
                self._handleReceivedData()),
        else:
            print("No arduino connection.")
