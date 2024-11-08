import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import math as m

#mapa
def drawMap(mapa,nazwaPliku):
    fig = plt.figure()
    plt.imshow(mapa)
    fig.savefig(nazwaPliku)

#wczytywanie danych
def loadMap(plik):
    with open(plik, 'r') as f:
        mapWidth, mapHeight, distance = map(int, f.readline().split())
        mapa = np.array([list(map(float, f.readline().split())) for _ in range(mapHeight)])
    return mapa, mapWidth, mapHeight, distance

#tworzenie macierzy HSV
def createHSVmatrix(mapHeight,mapWidth):
    hsvMatrix = []
    for i in range(mapHeight):
        hsvMatrix.append([])
        for j in range(mapWidth):
            hsvMatrix[i].append([0,1,1])
    return hsvMatrix


def hsv2rgb(h, s, v):
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    #okreslenie wartosci na podstawie sektora hsv
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    elif 300 <= h < 360:
        r, g, b = c, 0, x
    else:
        r, g, b = 0, 0, 0

    return [r + m, g + m, b + m]

#wektor normalny na powierzchni mapy
def calculateVectors(mapa, i, j, mapWidth, distance, mainPoint):
    if i % 2 == 0:
        if j < mapWidth-1:
            secondPoint = np.array([i*distance,mapa[i][j+1],distance*(j+1)]) #drugi punkt trojkata
            thirdPoint = np.array([(i+1)*distance,mapa[i+1][j],j*distance]) #trzeci punkt trojkata
        else:
            secondPoint = np.array([i * distance, mapa[i][j - 1], distance * (j - 1)])
            thirdPoint = np.array([(i + 1) * distance, mapa[i + 1][j], j * distance])
    else:
        if j > 0:
            secondPoint = np.array([i*distance,mapa[i][j-1],(j-1)*distance])
            thirdPoint = np.array([(i-1)*distance,mapa[i-1][j],j*distance])
        else:
            secondPoint = np.array([i * distance, mapa[i][j + 1], (j + 1) * distance])
            thirdPoint = np.array([(i - 1) * distance, mapa[i - 1][j], j * distance])


    normal = np.cross(secondPoint - mainPoint, thirdPoint - mainPoint) #wektor normalny powierzchni poprzez iloczyn wektorowy
    return normal

def calculateVectorSun(mainPoint, disntance):
    sun = np.array([-distance, 50, -distance])
    vectorToSun = sun - mainPoint #wektor kierujacy do slonca

    return vectorToSun
    

def vectorShading(mapa, mapHeight, mapWidth, distance):
    minimum = np.min(mapa) #min wysokosci do normalizacji
    maximum = np.max(mapa) - minimum #max wyskokosci do normalizacji
    mapaHSV = createHSVmatrix(mapHeight,mapWidth) #macierz wypelniona kolorami hsv
    matrixOfAngles = np.zeros([mapHeight,mapWidth]) #macierz katow miedzy sloncem a wektorem normalnym powierzchni
    
    for i in range(mapHeight):
        for j in range(mapWidth):
            mainPoint = np.array([i*distance,mapa[i][j],j*distance])
            normal = calculateVectors(mapa, i, j, mapWidth, distance, mainPoint)
            vectorToSun = calculateVectorSun(mainPoint, distance)

            #obliczanie kata miedzy wektorem normalnym i wektorem slonca
            angleSun = m.degrees(np.arccos(np.clip(np.dot(normal, vectorToSun)/(np.linalg.norm(normal)*np.linalg.norm(vectorToSun)),-1,1)))
            matrixOfAngles[i][j] = angleSun

    #posortowana lista katow dla lepszego cieniowania
    angles = np.sort(np.reshape(matrixOfAngles,-1))
    minAngle = np.min(angles)
    maxAngle = np.max(angles)

    #okreslanie stopnia przyciemnienia
    for i in range(mapHeight):
        for j in range(mapWidth):
            mapaHSV[i][j][0] = (1-((mapa[i][j]-minimum)/maximum)) * 120 #obliczenie odcienia

            normalized = ((matrixOfAngles[i][j]-minAngle)/(maxAngle-minAngle))*2 - 1  #w zakresie <-1,1>
            position = np.where(angles == matrixOfAngles[i][j])[0] #odchylenie kata od pozostalych
            position = position[0] / len(angles)

            #okreslenie s, v
            div = position - 0.5 
            if div < 0:
                mapaHSV[i][j][1] = 1 -np.sin(matrixOfAngles[i][j])*abs(div)
            else:
                mapaHSV[i][j][2] = 1 - np.sin(matrixOfAngles[i][j])*abs(div)

            #normalizowanie kata
            if normalized < 0:
                mapaHSV[i][j][1] = ((1+normalized) + mapaHSV[i][j][1])/2
            else:
                mapaHSV[i][j][2] = ((1-normalized) + mapaHSV[i][j][2])/2
            
            mapaHSV[i][j] = hsv2rgb(mapaHSV[i][j][0],mapaHSV[i][j][1],mapaHSV[i][j][2])
    
    return mapaHSV


mapa, mapHeight, mapWidth, distance = loadMap("big.dem")
mapaSimple = vectorShading(mapa,mapHeight,mapWidth,distance)
drawMap(mapaSimple,"simpleMap.pdf")
plt.close()