import sys
from collections import OrderedDict

inputFile = open(sys.argv[2], 'r')
#inputFile = open("///Users/weichuanli/Desktop/5611111/HW2/testcases/t17.txt", 'r')


color = inputFile.readline().strip()
color = color.split(",")
color = map(lambda x : x.strip(), color)
color.sort()

initialState = inputFile.readline().strip()
assigned = OrderedDict()
initialState = initialState.split(",")
for item in initialState:
    item.strip()
    item = item.split(":")
    list1 = item[1].split("-")
    list1 = map(lambda x : x.strip(), list1)
    assigned[item[0].strip()] = list1


maxDepth = int(inputFile.readline().strip())

preferenceForMax = inputFile.readline().strip()
preferenceForMax = preferenceForMax.split(",")
maxPreference = {}
for item in preferenceForMax:
    item = item.strip()
    item = item.split(":")
    maxPreference[item[0].strip()] = item[1].strip()


preferenceForMin = inputFile.readline().strip()
preferenceForMin = preferenceForMin.split(",")
minPreference = {}
for item in preferenceForMin:
    item = item.strip()
    item = item.split(":")
    minPreference[item[0].strip()] = item[1].strip()


remainingFile = inputFile.readlines()
neighbours = {}

for line in remainingFile:
    information = line.split(":")
    state = information[0]
    children = information[1].split(",")
    list2 = []
    for child in children:
        childName = child.strip()
        list2.append(childName)
    neighbours[state] = list2



inputFile.close()




allowedColor = {}
for state in neighbours:
    if state in assigned:
        list3 = [assigned[state][0]]
        allowedColor[state] = list3
    else:
        allowedColor[state] = color


def evaluation(assigned):
    maxSum =0
    minSum = 0
    for state, color in assigned.items():
        if int(color[1]) == 1:
            maxSum += int(maxPreference[(color[0])])
        else:
            minSum += int(minPreference[color[0]])

    return maxSum - minSum


def makeNextMove(assigned, move):


    state = move[0]
    color = move[1]
    player = move[2]
    assigned[state] = [color, player]


def cancelMove(assigned, move):
    assigned.pop(move[0])


def getNextMoves(assigned, player):
    possibleStatesSet = set()
    for state in assigned:
        for neigh in neighbours[state]:
            if neigh not in assigned:
                possibleStatesSet.add(neigh)


    possibleStates = sorted(possibleStatesSet)
    possibleMoves = []
    noColor = []


    for state in possibleStates:
        for colors in color:
            possibleMoves.append([state, colors])

    for state in assigned:
        for neighbour in neighbours[state]:
            if neighbour in possibleStatesSet:
                noColor.append([neighbour, assigned[state][0]])

    for nocolor in noColor:
        if nocolor in possibleMoves:
            possibleMoves.remove(nocolor)

    if player == max:
        for item in possibleMoves:
            item.append(1)
    elif player == min:
        for item in possibleMoves:
            item.append(0)
    return possibleMoves




def writeAtEnd(assigned, depth, alpha, beta, eval):
    item = next(reversed(assigned))
    color = assigned[item]
    file.write(
        item + ", " + color[0] +", "+ str(depth) + ", " + str(eval) + ", " + str(alpha) + ", " + str(
            beta) + '\n')

def write(assigned, depth, alpha, beta, v):
    item = next(reversed(assigned))
    color = assigned[item]
    file.write(item +", "+ color[0] +", "+ str(depth) + ", " + str(v) + ", " + str(alpha) + ", " + str(beta) + '\n')


def maxAlphaBeta(assigned, depth, alpha, beta, max):
    global bestScore
    global bestmove
    if depth == maxDepth or assigned.__len__() == neighbours.__len__():
        eval = evaluation(assigned)
        writeAtEnd(assigned, depth, alpha, beta, eval)
        return eval
    v = float('-inf')

    moves = getNextMoves(assigned, max)

    if moves.__len__() == 0:
        eval = evaluation(assigned)

        writeAtEnd(assigned, depth, alpha, beta, eval)
        return eval


    write(assigned, depth, alpha, beta, v)

    for move in moves:
        makeNextMove(assigned, move)
        v = max(v, minAlphaBeta(assigned, depth+1, alpha, beta, min))
        cancelMove(assigned, move)


        if depth == 0:
            if v > bestScore:
                bestScore = v
                bestmove = move

        if v >= beta:
            write(assigned, depth, alpha, beta, v)
            return v

        alpha = max(v, alpha)
        write(assigned, depth, alpha, beta, v)

    return v


def minAlphaBeta(assigned, depth, alpha, beta, min):

    if depth == maxDepth or assigned.__len__() == neighbours.__len__() :
        eval = evaluation(assigned)
        writeAtEnd(assigned, depth, alpha, beta, eval)
        return eval

    v = float("inf")
    moves = getNextMoves(assigned, min)


    if moves.__len__() == 0:
        eval = evaluation(assigned)
        writeAtEnd(assigned, depth, alpha, beta, eval)
        return eval




    write(assigned, depth, alpha, beta, v)

    for move in moves:
        makeNextMove(assigned, move)
        v = min(v,maxAlphaBeta(assigned, depth+1, alpha, beta, max))
        cancelMove(assigned, move)

        if v <= alpha:
            write(assigned, depth, alpha, beta, v)
            return v

        beta = min(v, beta)
        write(assigned, depth, alpha, beta, v)


    return v

bestScore = float("-inf")
bestmove = []
with open("output.txt",'w') as file:
    val = maxAlphaBeta(assigned, 0, float('-inf'), float('inf'),max)
    file.write(bestmove[0] + ", " + bestmove[1] + ", " + str(val))
