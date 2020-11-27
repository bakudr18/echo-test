import subprocess
import difflib
import sys
import os
import getopt

class Echotest:
    testDirectory = "./testcase"
    program = "./echo"
    command = program
    colored = False
    pydifflib = False
    fin = object()
    fout = object()
    testDict = {
        1: "input1.txt",
        2: "input2.txt",
        3: "input3.txt"
    }

    testProbs = {}
	
    RED = '\033[91m'
    GREEN = '\033[92m'
    WHITE = '\033[0m'
    
    def __init__(self, program = "", colored = False, pydifflib=False):
        if program != "":
            self.program = program
            self.command = self.program
        self.colored = colored
        self.pydifflib = pydifflib
    
    def printInColor(self, text, color):
        if self.colored == False:
            color = self.WHITE
        print(color, text, self.WHITE, sep = '')
    
    def runTest(self, tid):
        finname = "%s/%s" % (self.testDirectory, self.testDict[tid])
        foutname = "%s/output%d.txt" % (self.testDirectory, tid)
        try:
            with open(finname, 'r') as self.fin, \
                 open(foutname, 'w+') as self.fout:
                completed = subprocess.run(self.command, stdin=self.fin, stdout=self.fout)
                retcode = completed.returncode
                if retcode == 0:
                    self.testProbs[tid] = os.path.basename(self.fout.name)
                else:
                    self.printInColor("ERROR: Execute '%s' errno = %d" % (self.command, retcode) , self.RED)
                return retcode == 0
        except IOError as e:
            self.printInColor(e, self.RED)
            return False 
        except Exception as e:
            self.printInColor("Call of '%s' failed: %s" % (self.command, e), self.RED)
            return False

    def runDiff(self, tid):
        if not tid in self.testProbs:
            self.printInColor("Error: Invalid test ID %d in testProbs" % tid, self.RED)
            return False
        
        finname = "%s/%s" % (self.testDirectory, self.testDict[tid])
        foutname = "%s/%s" % (self.testDirectory, self.testProbs[tid])
        if not self.pydifflib:
            command = ['colordiff' if self.colored else 'diff']
            command += ["-u", "-s", finname, foutname]
            completed = subprocess.run(command)
            return completed.returncode == 0
        else:
            try:
                with open(finname, 'r') as self.fin, open(foutname, 'r') as self.fout:
                    finlines = self.fin.read().splitlines()
                    foutlines = self.fout.read().splitlines()
                    diff = False
                    for line in difflib.unified_diff(finlines, foutlines, fromfile=self.testDict[tid], tofile=self.testProbs[tid], lineterm="", n=0):
                        diff = True
                        color = self.WHITE
                        if line.startswith('-'):
                            color = self.RED
                        elif line.startswith('+'):
                            color = self.GREEN
                        self.printInColor(line, color)
                    if not diff:
                        self.printInColor("Files %s and %s are identical" % (finname, foutname), self.WHITE)
                return True
            except IOError as e:
                self.printInColor(e, self.RED)
                return False
            except Exception as e:
                self.printInColor(e, self.RED)
                return False

    def run(self, tid = 0):
        if tid == 0:
            tidList = self.testDict.keys()
        else:
            if not tid in self.testDict:
                self.printInColor("ERROR: Invalid test ID %d" % tid, self.RED)
                return
            tidList = [tid]
        
        for t in tidList: 
            ok = self.runTest(t)
            if ok:
                self.runDiff(t)

def usage(name):
    print("Usage: %s [-h] [-p PROG] [-t TID] [-c]" % name)
    print("  -h         Print this message")
    print("  -p PROG    Program to test")
    print("  -t TID     Test ID to test")
    print("  -c         Enable colored text")
    print("  --difflib  Use python difflib module")
    sys.exit(0)

def run(name, args):
    prog = ""
    tid = 0
    colored = False
    pydifflib = False

    optlist, args = getopt.getopt(args, 'h:p:t:c', 'difflib')
    for (opt, val) in optlist:
        if opt == '-h':
            usage(name)
        elif opt == '-p':
            prog = val
        elif opt == '-t':
            tid = int(val)
        elif opt == '-c':
            colored = True
        elif opt == '--difflib':
            pydifflib = True
        else:
            print("Unrecognized option '%s'" %opt)
            usage(name)
    et = Echotest(program=prog, 
                  colored=colored,
                  pydifflib=pydifflib)
    et.run(tid)

if __name__ == "__main__":
	run(sys.argv[0], sys.argv[1:])

