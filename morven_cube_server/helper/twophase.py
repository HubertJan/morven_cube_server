import subprocess as subprocess
import os as os
from time import sleep

class Twophase:
    
    @staticmethod
    def subprocess_cmd(pattern):
        process = subprocess.Popen("wsl helper/twophase",stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding='utf8')
        output = ""
        while(output != 'Ready!\n'):
            output = process.stdout.readline()
        os.write(process.stdin.fileno(), bytes("solve %s\n"%pattern, "utf-8"))
        output = os.read(process.stdout.fileno(), 4096).splitlines()
        instructions = output[1].decode("utf-8")
        instructions = instructions[:instructions.index("(")]
        process.kill()
        return instructions

    @staticmethod
    def solve(*args):
        output = Twophase.subprocess_cmd('DDFFURLFFLDRBRBFRFBLULFRUBDBLRRDFBULRUUFLUDURULBDBDDBL')
        return output

    @staticmethod
    def toArduinoFormat(solution):
        solList = list(solution.split(" "))
        improvedSolution = ""
        isFirst = True
        for ins in solList:
            if len(ins) == 1:
                ins = ins + "1"
            elif ins[1] == "'":
                ins = ins[0] + "7"
            if(isFirst):
                isFirst = False
            else:
                ins = " " + ins
            improvedSolution += ins
        return improvedSolution

print(Twophase.solve(""))