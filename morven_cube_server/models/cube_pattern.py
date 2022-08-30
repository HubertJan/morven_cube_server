from helper.cubeSimulator import CubeSimulator
from helper.kociemba_extend import Kociemba as kociemba

class CubePattern:
    def __init__(self, cubePatternString: str):
        self.pattern = cubePatternString

    

    def imposeInstructions(self, instructionString):
        self.pattern  = CubeSimulator.simulate(self.pattern, instructionString)

    def predictImposeInstructions(self, instructionString):
        calculatedPattern = CubeSimulator.simulate(self.pattern, instructionString)
        return calculatedPattern