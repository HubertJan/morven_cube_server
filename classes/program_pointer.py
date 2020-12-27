class ProgramPointer:
    def __init__(self, currentInstructionId, idString):
        self._currentInstructionId : str = currentInstructionId
        self._refId : str = idString
    
    @property
    def currentInstruction(self):
        return self._currentInstructionId
    
    @currentInstruction.setter
    def currentInstructionId(self, inp): 
        self._currentInstructionId = inp

    @property
    def id(self):
        return self._refId