import kociemba as koc


class Kociemba:
    @staticmethod
    def solve(*args) -> str:  # type: ignore
        if (args.__len__() == 1):
            solution = koc.solve(args[0])
        else:
            solution = koc.solve(args[0], args[1])
        return Kociemba.toArduinoFormat(solution)

    @staticmethod
    def toArduinoFormat(solution) -> str:  # type: ignore
        solList = list(solution.split(" "))
        improvedSolution = ""
        isFirst = True
        for ins in solList:
            if len(ins) == 1:
                ins = ins + "1"
            elif ins[1] == "'":
                ins = ins[0] + "7"
            if (isFirst):
                isFirst = False
            else:
                ins = " " + ins
            improvedSolution += ins
        return improvedSolution
