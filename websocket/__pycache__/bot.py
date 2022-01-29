import math


index = -1
deltaDistance = 60
xArr = []
yArr = []

def getNextSpawnPoint(x, y):
    global index
    global deltaDistance
    index +=1

    if index == 3:
        index = 0

    xArr = [int(x - deltaDistance*0.5), int(x + deltaDistance * 0.5), x ]
    yArr = [int(y + deltaDistance*0.5), int(y + deltaDistance* 0.5), int(y - deltaDistance * 0.5)]

    return [xArr[index], yArr[index]] 

def generateSpawnPointsSquare(x, y, count):
    global xArr
    global yArr
    
    sideSize = int(math.sqrt(count))
    for Y in range (int(sideSize/-2), int(sideSize/2)):
        for X in range(int(sideSize/-2), int(sideSize/2)):
            xArr.append(x + X * deltaDistance)
            yArr.append(y + Y * deltaDistance)

def getNextSpawnPoint(x, y, count):
    global index
    global deltaDistance
    index += 1

    if index == count:
        index = 0


    sideSize = int(math.sqrt(count))
    
    return [xArr[index], yArr[index]]