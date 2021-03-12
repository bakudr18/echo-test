import subprocess
import difflib
import sys
import os
import getopt

class Echotest:
    testDirectory = "./testcase"
    program = "./echo"
    pargs = []
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
    testLog = "log.txt"

    RED = '\033[91m'
    GREEN = '\033[92m'
    WHITE = '\033[0m'
    
    def __init__(self, program = "", pargs = [], colored = False, pydifflib=False):
        if program != "":
            self.program = program
            self.command = self.program
            if pargs:
                self.pargs = pargs
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
                cmd = [self.command] + self.pargs
                completed = subprocess.run(cmd, stdin=self.fin, stdout=self.fout, stderr=subprocess.STDOUT)
                self.testProbs[tid] = os.path.basename(self.fout.name)
                return completed.returncode
        except IOError as e:
            self.printInColor(e, self.RED)
            return -e.errno 
        except Exception as e:
            self.printInColor("Call of '%s' failed: %s" % (self.command, e), self.RED)
            return -1

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
    
    def showLog(self, tid, ret):
        self.printInColor("Get returncode %d from %s run test" % (ret, self.program), self.RED)
        stdout = os.path.join(self.testDirectory, self.testProbs[tid]);
        log = os.path.join(self.testDirectory, self.testLog)
        os.rename(stdout, log);
        try:
            with open(log, 'r') as l:
                lines = l.read().splitlines();
                for line in lines:
                    self.printInColor(line, self.WHITE)
        except Exception as e:
            self.printInColor(e, self.RED)

    def run(self, tid = 0):
        if tid == 0:
            tidList = self.testDict.keys()
        else:
            if not tid in self.testDict:
                self.printInColor("ERROR: Invalid test ID %d" % tid, self.RED)
                return
            tidList = [tid]
        
        for t in tidList: 
            ret = self.runTest(t)
            if ret == 0:
                self.runDiff(t)
            else:
                self.showLog(t, ret)

def usage(name):
    print("Usage: %s [--args] PROGRAM [OPTIONS]" % name)
    print("  PROGRAM                        execute program")
    print("  --args PROGRAM arg1 arg2 ...   execute program with args")
    print("  -h                             Print this message")
    print("  -t TID                         Test ID to test")
    print("  -c                             Enable colored text")
    print("  --difflib                      Use python difflib module")
    sys.exit(0)

def run(name, args):
    prog = ""
    pargs = []
    tid = 0
    colored = False
    pydifflib = False
    
    if(args[0] != '-h' and args[0] != '--args'):
        prog = args[0]
        args = args[1:]
    elif args[0] == '--args':
        prog = args[1]
        args = args[2:]
        while args[0][0] != '-':
            pargs.append(args.pop(0))
            
    optlist, args = getopt.getopt(args, 'hct:', 'difflib')
    for (opt, val) in optlist:
        if opt == '-h':
            usage(name)
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
                  pargs=pargs,
                  colored=colored,
                  pydifflib=pydifflib)
    et.run(tid)

if __name__ == "__main__":
	run(sys.argv[0], sys.argv[1:])

