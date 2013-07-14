#!/usr/bin/python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE

def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    process = Popen(['ruby', 'solver.rb'], stdin=PIPE, stdout=PIPE)
    (stdout, stderr) = process.communicate(inputData)

    return stdout.strip()

import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'

