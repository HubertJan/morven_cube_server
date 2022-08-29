import uuid
import asyncio
import time
from aiohttp import web
from datetime import datetime
from enum import Enum
from morven_cube_server.provide import provide

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
            self._mainArduinoConnection = ArduinoConnection("/COM3", 115200)
         #   self._secondaryArduinoConnection = STMConnector("COM16", 115200)
            self._cubePattern = None
            self._currentProgram: Program = None
            self._currentInstructionId = None
            self._programRunningTime = 0
            self._server = web.Application()
            self._sensorData = {
                "temp1": 0,
                "temp2": 0,
                "temp3": 0,
                "volt1": 0,
                "volt2": 0,
                "volt3": 0,
            }
        except:
            return

    @property
    def _futureCubePattern(self):
        return self._cubePattern.pattern


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
        #    self._secondaryArduinoConnection.sendLight("BL")
       #     self._secondaryArduinoConnection.sendLight("WH")
     #   self._secondaryArduinoConnection.sendMotor("OP")
        #    self._secondaryArduinoConnection.sendLight("BL")
      #      self._secondaryArduinoConnection.sendLight("WH")
       #     self._secondaryArduinoConnection.sendMotor("CL")
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
                data: dict = self._secondaryArduinoConnection.receivedInfo
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
                self._secondaryArduinoConnection.receivedInfo.clear()

    async def setupSecondary(self):
        self._toVerifyPattern = CubePattern(self._getCamData())
       # await self._secondaryArduinoConnection.sendSetSensor()

    async def runService(self):
        await self._mainArduinoConnection.connect()
       # await self._secondaryArduinoConnection.connect()
        self._cubePattern = CubePattern(
            "DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD")
        if(self._mainArduinoConnection.isConnected()): #and self._secondaryArduinoConnection.isConnected()):

            self._server.router.add_routes(self._routes)
            await asyncio.gather(
                web._run_app(self._server,  host='localhost', port=9000),
                self._mainArduinoConnection.loopReceivingData(),
                self._handleReceivedData(),
                #self._secondaryArduinoConnection.loopReceivingData(),
              #  self._handleReceivedDataSecondary(),
                self.setupSecondary()),
        else:
            print("No arduino connection.")

def connect_and_update_sensor_data(app: web.Application):
    arduinoServce = STMConnector()
    app["secondaryArduino"] = 

def run_server():
    app = web.Application()
    provide(app=app, value=ServerState)
    app.on_startup()