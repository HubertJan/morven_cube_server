import uuid
import asyncio
import time
from aiohttp import web
from datetime import datetime
from enum import Enum
from morven_cube_server.models.server_state import ServerState
from morven_cube_server.provide import provide

from helper.kociemba_extend import Kociemba as kociemba
from helper.cubeSimulator import CubeSimulator
from helper.stoppWatch import StoppWatch
from morven_cube_server.services.arduino_connection import connect_to_arduino
from morven_cube_server.services.database import RubiksDatabase
from morven_cube_server.services.primary_arduino_service import PrimaryArduinoService
from morven_cube_server.services.secondary_arduino_connection import SecondaryArduinoService

def run_server():
    app = web.Application()

    provide(app=app, value=PrimaryArduinoService(), valueType=PrimaryArduinoService)
    provide(app=app, value=SecondaryArduinoService(), valueType=SecondaryArduinoService)
    provide(app=app, value=ServerState(), valueType=ServerState)
    web.run_app(app, host='localhost', port=9000)