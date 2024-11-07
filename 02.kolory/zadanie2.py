import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import math as m

# Funkcja rysująca mapę
def drawMap(mapa,nazwaPliku):
    fig = plt.figure()
    plt.imshow(mapa)
    plt.show()
    fig.savefig(nazwaPliku)

# Wczytywanie punktów na mapie oraz wyskości, szerokości mapy i dystansu między punktami
def loadMapPoints(fileName):
    with open(fileName) as file:
        mapa = file.read().splitlines()
    mapa = [i.split(' ') for i in mapa]
    mapHeight= int(mapa[0][0]) # wysokość mapy
    mapWidth = int(mapa[0][1]) # szerokość mapy
    distance = int(mapa[0][2]) # dystans pomiędzy punktami
    del mapa[0]
    for i in range(len(mapa)):
        del mapa[i][-1]
        mapa[i] = [ float(point) for point in mapa[i]] # Zamiana łańcucha znaków na float
    return mapa,mapWidth,mapHeight,distance

# Tworzenie macierzy kolorów HSV
def createHSVmatrix(mapHeight,mapWidth):
    hsvMatrix = []
    for i in range(mapHeight):
        hsvMatrix.append([])
        for j in range(mapWidth):
            hsvMatrix[i].append([0,1,1])
    return hsvMatrix


def hsv2rgb(h, s, v):
    vs = v*s
    if h > 0:
        while h > 360:
            h -= 360
    else:
        while h < 0:
            h += 360
    hue = h/60
    x = vs * (1 - abs((hue % 2) -1))
    # W zależności od tego w jakiej cześci okręgu się znajduje kolor
    switcher = {
        0: [vs,x,0],
        1: [x,vs,0],
        2: [0,vs,x],
        3: [0,x,vs],
        4: [x,0,vs],
        5: [vs,0,x],
        6: [vs,x,0]
    }
    rgb = switcher.get(m.trunc(hue),[0,0,0])
    match = v-vs
    rgb = [i+match for i in rgb]
    return rgb


def simpleShading(mapa,mapHeight,mapWidth,distance):
    minimum = np.min(mapa)  # Minimum wysokości potrzebne do normalizacji
    maximum = np.max(mapa) - minimum# Maximum wyskokości potrzebne do normalizacji
    mapaHSV = createHSVmatrix(mapHeight, mapWidth)  # Macierz, która jest uzupełniana kolorami HSV na podstawie obliczeń
    for i in range(mapHeight):
        for j in range(mapWidth):
            # Obliczanie koloru między zielonym (120 - hue) a czerwonym (0)
            mapaHSV[i][j][0] = (1 - ((mapa[i][j] - minimum) / maximum)) * 120
            if j == 0:
                div = mapa[i][j] - mapa[i][j+1] # Różnica między wysokością punktu a jego prawym sąsiadem
            else:
                div = mapa[i][j] - mapa[i][j-1] # Różnica między wysokością punktu a jego lewym sąsiadem
            div = div*7 / maximum
            if div > 0:
                mapaHSV[i][j][1] -= abs(div)
            else:
                mapaHSV[i][j][2] -= abs(div)
            mapaHSV[i][j] = hsv2rgb(mapaHSV[i][j][0], mapaHSV[i][j][1], mapaHSV[i][j][2])
    return mapaHSV

if __name__ == '__main__':
    mapa, mapHeight, mapWidth, distance = loadMapPoints("big.dem")
    mapaSimple = simpleShading(mapa,mapHeight,mapWidth,distance)
    drawMap(mapaSimple,"simpleMap.pdf")
    plt.close()