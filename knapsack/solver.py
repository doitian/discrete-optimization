#!/usr/bin/python
# -*- coding: utf-8 -*-

def dynamicProgramming(items, values, weights, capacity):
    # Build matrix
    objectiveMatrix = [[0 for x in xrange(capacity + 1)] for x in xrange(items + 1)]
    for i in range(1, items + 1):
        value = values[i - 1]
        weight = weights[i - 1]
        prev = objectiveMatrix[i - 1]
        row = objectiveMatrix[i]

        for currentCapacity in range(0, capacity + 1):
            row[currentCapacity] = prev[currentCapacity]
            if currentCapacity >= weight:
                objectiveToTakeCurrentItem = prev[currentCapacity - weight] + value
                if objectiveToTakeCurrentItem > row[currentCapacity]:
                    row[currentCapacity] = objectiveToTakeCurrentItem


    # backtrace
    taken = [0] * items
    remainingCapacity = capacity
    for i in range(items, 0, -1):
      if objectiveMatrix[i][remainingCapacity] != objectiveMatrix[i - 1][remainingCapacity]:
          remainingCapacity -= weights[i - 1]
          taken[i - 1] = 1

    # print objectiveMatrix

    return objectiveMatrix[items][capacity], taken

def greedyValuePerWeight(items, values, weights, capacity):
    # sort by value/weight
    sortedIndexes = sorted(range(0, items), key=lambda i: - float(values[i]) / weights[i])
    taken = [0] * items
    value = 0
    weight = 0
    for i in sortedIndexes:
        if weight + weights[i] <= capacity:
            value += values[i]
            weight += weights[i]
            taken[i] = 1

    return value, taken

def greedyValue(items, values, weights, capacity):
    # sort by value/weight
    sortedIndexes = sorted(range(0, items), key=lambda i: - values[i])
    taken = [0] * items
    value = 0
    weight = 0
    for i in sortedIndexes:
        if weight + weights[i] <= capacity:
            value += values[i]
            weight += weights[i]
            taken[i] = 1

    return value, taken

def sortedBranchAndBondWithLinearRelaxation(items, values, weights, capacity):
    bestValue, bestTaken = greedyValuePerWeight(items, values, weights, capacity)
    if bestValue == 0 or not (0 in bestTaken):
        return bestValue, bestTaken

    taken = [0] * items
    takenValue = 0
    takenWeight = 0
    estimation = 0
    i = 0

    while i >= 0:
        memo = (i, takenValue, takenWeight)
        while i < items and takenWeight < capacity:
            taken[i] = 1
            takenValue += values[i]
            takenWeight += weights[i]
            i += 1

        estimation = takenValue
        if takenWeight > capacity:
            estimation -= (takenWeight - capacity) * (float(values[i - 1]) / weights[i - 1])

        # collect solution
        if i == items:
            value = takenValue
            if takenWeight > capacity:
                value = takenValue - values[-1]
                taken[-1] = 0

            if value > bestValue:
                bestValue = value
                bestTaken = taken[:]

            takenValue -= values[-1]
            takenWeight -= weights[-1]
            i = items - 1

        # print '---------'
        # print i, taken[0:i], takenValue, takenWeight, estimation, bestValue, memo

        if estimation <= bestValue:
            # prune the branch
            i, takenValue, takenWeight = memo

        i -= 1
        while i >= 0 and taken[i] == 0:
            i -= 1

        if i >= 0:
            takenValue -= values[i]
            takenWeight -= weights[i]
            taken[i] = 0
            i += 1

        # print i, taken[0:i], takenValue, takenWeight

    return bestValue, bestTaken

# Sort by value and use depth first search.
#
# Use greedy as a base solution.
def branchAndBondWithLinearRelaxation(items, values, weights, capacity):
    sortedIndexes = sorted(range(0, items), key=lambda i: - float(values[i]) / weights[i])
    values = [values[i] for i in sortedIndexes]
    weights = [weights[i] for i in sortedIndexes]

    value, sortedTaken = sortedBranchAndBondWithLinearRelaxation(items, values, weights, capacity)

    taken = [0] * items
    for i in range(0, items):
        taken[sortedIndexes[i]] = sortedTaken[i]

    return value, taken

def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    items = int(firstLine[0])
    capacity = int(firstLine[1])

    values = []
    weights = []

    for i in range(1, items+1):
        line = lines[i]
        parts = line.split()

        values.append(int(parts[0]))
        weights.append(int(parts[1]))

    if True: # capacity > items and capacity >= 100000:
        # Large input size, use greedy
        opt = 0
        # value, taken = greedyValuePerWeight(items, values, weights, capacity)
        # value, taken = greedyValue(items, values, weights, capacity)
        opt = 1
        value, taken = branchAndBondWithLinearRelaxation(items, values, weights, capacity)
    else:
        opt = 1
        value, taken = dynamicProgramming(items, values, weights, capacity)

    # prepare the solution in the specified output format
    outputData = str(value) + ' ' + str(opt) + '\n'
    outputData += ' '.join(map(str, taken))
    return outputData


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

