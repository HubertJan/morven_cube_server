from morven_cube_server.helper.kociemba_extend import Kociemba as kociemba
# from pyTwistyScrambler import scrambler333


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
    def simulate(patternString: str, instructionsString: str) -> str:
        instructions = list(instructionsString.split(" "))
        pattern = patternString
        if instructions.__len__() == 0 or instructions[0] == "":
            return patternString
        for instruction in instructions:
            for instructionRef in CubeSimulator.instructionDic:
                if (instruction[0] == instructionRef):
                    if (instruction[1] == "1"):
                        pattern = CubeSimulator._swap_character(
                            CubeSimulator.instructionDic[instructionRef], pattern, True)
                    elif (instruction[1] == "7"):
                        pattern = CubeSimulator._swap_character(
                            CubeSimulator.instructionDic[instructionRef], pattern, clockwise=False)
                    elif (instruction[1] == "2"):
                        pattern = CubeSimulator._swap_character(
                            CubeSimulator.instructionDic[instructionRef], pattern, is_rotation_180=True)
                    break
        returnPattern = "".join(pattern)
        return returnPattern

    @staticmethod
    def _swap_character(to_change_rows: list[list[int]], pattern: str, clockwise: bool = True, is_rotation_180: bool = False) -> str:
        row_integer = to_change_rows[0]
        cube_circle = to_change_rows[1]
        if is_rotation_180:
            x = 2
        else:
            if (clockwise):
                x = 1
            else:
                x = -1
        pattern_as_list = list(pattern)
        new_pattern_as_list = list(pattern)

        for i in range(0, row_integer.__len__()):
            if i + 3 * x >= row_integer.__len__():
                index = row_integer[i + 3 * x - row_integer.__len__()]
            elif i + 3 * x < 0:
                index = row_integer[i + 3 * x + row_integer.__len__()]
            else:
                index = row_integer[i + 3 * x]
            new_pattern_as_list[row_integer[i]] = pattern_as_list[index]
        for i in range(0, cube_circle.__len__()):
            if i - 2 * x < 0:
                index = cube_circle[i - 2 * x + cube_circle.__len__()]
            elif i - 2 * x >= cube_circle.__len__():
                index = cube_circle[i - 2 * x - cube_circle.__len__()]
            else:
                index = cube_circle[i - 2 * x]
            new_pattern_as_list[cube_circle[i]] = pattern_as_list[index]
        return ''.join(new_pattern_as_list)

    @staticmethod
    def validate_instructions(instructions_string: str) -> bool:
        instructions = list(instructions_string.split(" "))
        for instruction in instructions:
            isValid = False
            for instructionRef in CubeSimulator.instructionDic:
                if (instruction[0] == instructionRef):
                    isValid = True
            if (isValid == False):
                return False
        return True

    @staticmethod
    def generate_scramble() -> str:
        return CubeSimulator.to_format("DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD")

    @staticmethod
    def to_format(solution: str) -> str:
        solList = list(solution.split(" "))
        improvedSolution = ""
        isFirst = True
        for ins in solList:
            if len(ins) == 1:
                ins = ins + "1"
            elif ins[1] == "'":
                ins = ins[0] + "3"
            if (isFirst):
                isFirst = False
            else:
                ins = " " + ins
            improvedSolution += ins
        return improvedSolution

    @staticmethod
    def validate_pattern(patternString: str) -> bool:
        pattern = list(patternString)
        colorCounters = {}
        instDic = CubeSimulator.instructionDic
        for instructionRef in instDic:
            colorCounters[instructionRef] = 0

        for counterRef in colorCounters:
            cubeSide = instDic[counterRef][1]
            middleCubeSide = int((cubeSide[4]-cubeSide[0]) / 2 + cubeSide[0])
            if (pattern[middleCubeSide] != counterRef):
                return False
        for field in pattern:
            if (colorCounters[field] is None):
                return False
            colorCounters[field] += 1
        for counterRef in colorCounters:
            if colorCounters[counterRef] != 9:
                return False
        return True

    @staticmethod
    def _print_one_cube(v) -> None:   # type: ignore
        print("             |************|")
        for index in range(0, 3):
            i = index * 3
            print(f"             |*-{v[i]}**-{v[i+1]}**-{v[i+2]}*|")
            print("             |************|")

    @staticmethod
    def _print_four_cubes(c1, c2, c3, c4) -> None:  # type: ignore
        print(" ************|************|************|************")
        for index in range(0, 3):
            i = index * 3
            print(f" *-{c1[i]}**-{c1[i+1]}**-{c1[i+2]}*|*-{c2[i]}**-{c2[i+1]}**-{c2[i+2]}*|*-{c3[i]}**-{c3[i+1]}**-{c3[i+2]}*|*-{c4[i]}**-{c4[i+1]}**-{c4[i+2]}*")
            print(" ************|************|************|************")

    @staticmethod
    def print_rubiks_cube(pa):   # type: ignore
        CubeSimulator._print_one_cube(pa[0:9])
        CubeSimulator._print_four_cubes(
            pa[36:45], pa[18:27], pa[9:18], pa[45:54])
        CubeSimulator._print_one_cube(pa[27:36])
