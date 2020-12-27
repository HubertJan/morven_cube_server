from helper.kociemba_extend import Kociemba as kociemba


class CubeSimulator:

    instructionDic = {
            "U": [
                [
                    9, 10, 11,
                    45, 46, 47,
                    36, 37, 38,
                    18, 19, 20,
                ],
                [0, 1, 2, 5, 8, 7, 6, 3],
            ],
            "F": [
                [
                    38, 41, 44,
                    27, 28, 29,
                    15, 12, 9,
                    8, 7, 6, ],
                [18, 19, 20, 23, 26, 25, 24, 21, ],
            ],
            "D": [
                [
                    26, 25, 24,
                    44, 43, 42,
                    53, 52, 51,
                    17, 16, 15, ],
                [27, 28, 29, 32, 35, 34, 33, 30, ],
            ],
            "R":  [
                [
                    20, 23, 26,
                    29, 32, 35,
                    51, 48, 45,
                    2, 5, 8, ],
                [9, 10, 11, 14, 17, 16, 15, 12, ],
            ],
            "B":   [
                [
                    11, 14, 17,
                    35, 34, 33,
                    42, 39, 36,
                    0, 1, 2, ],
                [45, 46, 47, 50, 53, 52, 51, 48, ]
            ],
            "L": [
                [
                    33, 30, 27,
                    24, 21, 18,
                    6, 3, 0,
                    47, 50, 53, ],
                [36, 37, 38, 41, 44, 43, 42, 39, ],
            ],
        }

    @staticmethod
    def simulate(patternString: str, instructionsString: str):
        instructions = list(instructionsString.split(" ")) 
        pattern = list(patternString)
        if instructions.__len__() == 0 or instructions[0] == "":
            return patternString
        for instruction in instructions:
            for instructionRef in CubeSimulator.instructionDic:
                if (instruction[0] == instructionRef):
                    if(instruction[1] == "1"):
                        pattern = CubeSimulator._swapCharacter(
                            CubeSimulator.instructionDic[instructionRef], pattern, True)
                    elif(instruction[1] == "7"):
                        pattern = CubeSimulator._swapCharacter(
                            CubeSimulator.instructionDic[instructionRef], pattern, clockwise=False)
                    elif(instruction[1] == "2"):
                        pattern = CubeSimulator._swapCharacter(
                            CubeSimulator.instructionDic[instructionRef], pattern, rotation180=True)
                    break
        returnPattern = "".join(pattern)
        return returnPattern

    @staticmethod
    def _swapCharacter(toChangeRows, pattern, clockwise=True, rotation180=False):
        rowInteger = toChangeRows[0]
        cubeCircle = toChangeRows[1]
        if rotation180:
            x = 2
        else:
            if(clockwise):
                x = 1
            else:
                x = -1
        patternAsList = list(pattern)
        newPatternAsList = list(pattern)
        
        for i in range(0, rowInteger.__len__()):
            if i + 3 * x >= rowInteger.__len__():
                index = rowInteger[i + 3 * x - rowInteger.__len__()]
            elif i + 3 * x < 0:
                index = rowInteger[i + 3 * x + rowInteger.__len__()]
            else:
                index = rowInteger[i + 3 * x]
            newPatternAsList[rowInteger[i]] = patternAsList[index]
        for i in range(0, cubeCircle.__len__()):
            if i - 2 * x < 0:
                index = cubeCircle[i - 2 * x + cubeCircle.__len__()]
            elif i - 2 * x >= cubeCircle.__len__():
                index = cubeCircle[i - 2 * x - cubeCircle.__len__()]
            else:
                index = cubeCircle[i - 2 * x]
            newPatternAsList[cubeCircle[i]] = patternAsList[index]
        return ''.join(newPatternAsList)

    @staticmethod
    def validCheckOfInstructions(instructionsString):
        instructions = list(instructionsString.split(" "))
        for instruction in instructions:
            isValid = False
            for instructionRef in CubeSimulator.instructionDic:
                if (instruction[0] == instructionRef):
                    isValid = True
            if(isValid == False):
                return False
        return True

    @staticmethod
    def validCheckOfPattern(patternString):
        pattern = list(patternString)
        colorCounters = {};
        instDic = CubeSimulator.instructionDic
        for instructionRef in instDic:
            colorCounters[instructionRef] = 0

        for counterRef in colorCounters:
            cubeSide = instDic[counterRef][1]
            middleCubeSide = int((cubeSide[4]-cubeSide[0]) / 2 + cubeSide[0])
            if(pattern[middleCubeSide] != counterRef):
                return False
        for field in pattern:
            if(colorCounters[field] == None):
                return False
            colorCounters[field] += 1;
        for counterRef in colorCounters:
            if colorCounters[counterRef] != 9:
                return False
        return True

    @staticmethod
    def _printOneCube(v):
        print("             |************|")
        for index in range(0, 3):
            i = index * 3
            print(f"             |*-{v[i]}**-{v[i+1]}**-{v[i+2]}*|")
            print("             |************|")


    @staticmethod
    def _print4Cubes(c1, c2, c3, c4):
        print(" ************|************|************|************")
        for index in range(0, 3):
            i = index * 3
            print(f" *-{c1[i]}**-{c1[i+1]}**-{c1[i+2]}*|*-{c2[i]}**-{c2[i+1]}**-{c2[i+2]}*|*-{c3[i]}**-{c3[i+1]}**-{c3[i+2]}*|*-{c4[i]}**-{c4[i+1]}**-{c4[i+2]}*")
            print(" ************|************|************|************")

    @staticmethod
    def printRubiksCube(pa):
        _printOneCube(pa[0:9])
        _print4Cubes(pa[36:45], pa[18:27], pa[9:18], pa[45:54])
        _printOneCube(pa[27:36])