import kociemba
import serial

from aiohttp import web
import json
import asyncio
import time
import datetime


class ArduinoConnection:
    def __init__(self):
        print("Connection established")
        self.arduino = serial.Serial('COM6', 9600)
        self.arduino.readline()
        time.sleep(.1)

    def sendActions(self, actions):
        self._sendCommand("solve")

    @property
    def status(self):
        sta = self._sendCommand("status")
        return sta

    # return index number of current action in action string
    def getCurrentActionIndex(self):
        sta = self._sendCommand("currentActionIndex")
        return sta

    def _sendCommand(self, commandString):
        commandString = commandString + "\n"
        self.arduino.write(commandString.encode())
        data = self.arduino.readline()
        dataString = str(data)
        return dataString[2:len(dataString)-5]


class Machine:
    def __init__(self, ):
        self._connection = ArduinoConnection()
        self._cubePattern = None
        self._latestAppliedAction = None
        self._DateOfCamData = None
        self._actions = None
        self._routes = [
            web.get("/status", self.respGetStatus),
            web.get("/actionPlan", self.respGetActionPlan),
            web.post("/actionPlan/{arguments}", self.respPostActionPlan),
            web.get("/pattern", self.respGetPattern),
            web.post("/pattern/{arguments}", self.respPostPattern),
        ]

    def respGetStatus(self, request):
        sta = self._connection.status;

        if(sta == "working"):
            resp = web.json_response(
                {
                    "status": sta,
                    "currentActionID": self._connection.getCurrentActionIndex(),
                }
            )
        else:
            resp = web.json_response(
                {
                    "status": sta,
                    "currentActionID": None,
                }
            )
      
        return resp
    
    def respGetActionPlan(self, request):
        resp = web.json_response(
            {
                "currentActionPlan": self._actions,
            }
        )
        return resp

    def respPostActionPlan(self, request):
        arduinoResponse = self._connection.sendActions()
        resp = web.json_response(
            {
                "message": arduinoResponse,
            }
        )
        return resp
    
    def respGetPattern(self, request):
        resp = web.json_response(
            {
                "currentPattern": self.cubePattern,
                "futurePattern": self.futurePattern,
            }
        )
        return resp
    
    def respPostPattern(self, request):
        if("" == "solve"):
            arduinoResponse = self.solveRubiks()
        else:
            arduinoResponse = self.solveRubiks()
        resp = web.json_response(
            {
                "message": arduinoResponse,
            }
        )
        return resp

    @property
    def cubePattern(self):
        if self._cubePattern == None:
            self._cubePattern = self.getCamData()
        elif self._actions == None:
            return self._cubePattern
        else:
            currentActionIndex = self.getCurrentAction()
            if(currentActionIndex > len(self._actions)):
                self._cubePattern = self._calculateCubePattern(
                    self._actions[:])
            else:
                return self._calculateCubePattern(self._actions[:currentActionIndex])

        return self._cubePattern

    @cubePattern.deleter
    def cubePattern(self):
        del self._cubePattern

    def applyActionsOnCubePattern(self):
        # self._latestAppliedAction = self._actions Set to last action id
        # Apply all changes through actions to the cubePattern
        print("applyActionOnCubePattern")

    def runServer(self):
        app = web.Application()
        app.router.add_routes(self._routes)
        web.run_app(app,  host='localhost', port=9000)


    def solveRubiks(self):
        self._actions = kociemba.solve(self.getCamData())
        self._connection.sendActions(self._actions)
        return
    
    def solveRubiks(self, pattern):
        self._actions = kociemba.solve(self.getCamData(), patternstring=pattern)
        self._connection.sendActions(self._actions)
        return

    def calculateCubePattern(self, actions):
        return self._cubePattern

    def getCamData(self):
        print("Receiving camData.")
        time.sleep(5)
        return 'DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD'


machine = Machine()
machine.runServer()
