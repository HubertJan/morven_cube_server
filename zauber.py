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
from classes.cube_pattern import CubePattern
from helper.cubeSimulator import CubeSimulator
from classes.program import Program
from classes.program_pointer import ProgramPointer
from helper.stoppWatch import StoppWatch


class Zauber:
    def __init__(self, ):
        try:
            self._db = RubiksDatabase("/db_cube.csv")
            self._arduinoConnection = ArduinoConnection("COM6", 9600)
            self._cubePattern = CubePattern(self._getCamData())
            self._currentProgram: Program = None
            self._status = "NOT FETCHED"
            self._currentInstructionId = None
            self._programRunningTime = 0
            self._server = web.Application()
            self._routes = [
                web.get("/status", self.handlerGetStatus),
                web.patch("/status/{arguments}", self.handlerPatchStatus),
                web.get("/program", self.handlerGetProgram),
                web.post("/program/{arguments}", self.handlerPostProgram),
                web.get("/pattern", self.handlerGetPattern),
                web.post("/pattern/{arguments}", self.handlerPostPattern),
                web.get("/records", self.handlerGetRecords),
            ]
        except:
            return

    @property
    def _futureCubePattern(self):
        return self._cubePattern.pattern

    async def handlerGetStatus(self, request):
        resp = web.json_response(
            {
                "status": self._status,
                "program":  self._currentProgram.instructions if self._currentProgram.instructions != None else "",
                "programId": self._currentProgram.id if self._currentProgram.id != None else "",
                "currentInstructionId": self._currentInstructionId if self._currentInstructionId != None else "",
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
                "startPattern": self._cubePattern.pattern,
                "endPattern": self._futureCubePattern,
                "time": self._programRunningTime.runningTime,
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
        await self._arduinoConnection.sendStatus(command)
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

    async def handlerPostPattern(self, request):
        if(self._status == "RUN"):
            return web.json_response(
                {
                    "msg": "A program is already running."
                },
                status=403)
        command = request.rel_url.name
        if(command == "solve" or command == ""):
            inst = kociemba.solve(self._cubePattern.pattern)
            resp = await self._createAndSendProgramByInstructions(inst)
        else:
            resp = await self._createAndSendProgramByPattern(command)
        return resp

    async def handlerGetRecords(self, request):
        resp = web.json_response(
            {
                "records": self._db.records,
            },
            status=200
        )
        return resp

    async def _createAndSendProgramByInstructions(self, instructions: str):
        if(CubeSimulator.validCheckOfInstructions(instructions) == False):
            return web.json_response(
                {
                    "msg": "Invalid instructions",
                },
                status=400
            )
        programId = uuid.uuid4().hex
        programData = await self._arduinoConnection.sendProgram(instructions, programId)
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

    async def _createAndSendProgramByPattern(self, pattern: str):
        if(CubeSimulator.validCheckOfPattern(pattern)):
            inst = kociemba.solve(self._cubePattern.pattern, pattern)
            return await self._createAndSendProgramByInstructions(inst)
        else:
            return web.json_response(
                {
                    "msg": "Invalid pattern",
                },
                status=400
            )

    def _getCamData(self):
        print("Receiving camData.")
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
            if(len(self._arduinoConnection.receivedInfo) == 0):
                await asyncio.sleep(0)
            else:
                data: dict = self._arduinoConnection.receivedInfo
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
                self._arduinoConnection.receivedInfo.clear()

    async def runService(self):
        await self._arduinoConnection.connect()
        if(self._arduinoConnection.isConnected()):
            self._server.router.add_routes(self._routes)
            await asyncio.gather(
                web._run_app(self._server,  host='localhost', port=9000),
                self._arduinoConnection.loopReceivingData(),
                self._handleReceivedData()),
        else:
            print("No arduino connection.")
