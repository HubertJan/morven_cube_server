from helper.cubeSimulator import CubeSimulator

class Program:
    def __init__(self, instructionsString, idString, startPattern):
        self._instructions : str = instructionsString
        self._id : str = idString
        self._startPattern: str = startPattern
        self._endPattern = CubeSimulator.simulate(startPattern, instructionsString)
        self._is_manual: bool = False
    
    @property
    def endPattern(self):
        return self._endPattern

    @property
    def startPattern(self):
        return self._startPattern

    @property
    def instructions(self):
        return self._instructions

    @property
    def id(self):
        return self._id
    
    @property
    def length(self):
        if(self._instructions == ""):
            return 0
        return self._instructions.count(" ") + 1

    @property
    def reversedProgram(self):
        reversedProgram = list(self._instructions.split(" "))
        reversedProgram.reverse()
        for i, instruction in enumerate(reversedProgram):
            if len(reversedProgram[i]) == 1:
                reversedProgram[i] = reversedProgram[i][0] + "'"
            elif reversedProgram[i][1] == "'":
                reversedProgram[i] = reversedProgram[i][0]
        return reversedProgram