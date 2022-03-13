import csv
import math
import random
import numpy
import matplotlib.pyplot as plot
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

def Evkl(vx, vy):
    # Метрика Евклида
    sum = 0
    for k in range(len(vx)):
        sum = sum + (vx[k] - vy[k]) ** 2
    return float('{:.2f}'.format(math.sqrt(sum)))

def GetMatrix (name):
    results = []
    with open(name, newline='') as File:
        reader = csv.reader(File)
        for row in reader:
            row.pop(0)
            if len(row) > 9:
                row.pop(9)
            results.append(row)
    results.pop(0)
    for i in range(len(results)):
        for j in range(len(results[i])):
            results[i][j] = float(results[i][j].replace(',', '.'))
    return results

def MaxRass(clusters):
    '''
    minR = math.inf
    for cl1 in clusters:
        for cl2 in clusters:
            if cl1 != cl2:
                rass = Evkl(cl1, cl2)
                if rass < minR:
                    minR = rass
    return minR / len(clusters)'''
    sum = 0
    count = 0
    for i in range(0, len(clusters)):
        for j in range(i, len(clusters)):
            if i != j:
                sum = sum + Evkl(clusters[i], clusters[j])
                count = count + 1
    return float('{:.2f}'.format(sum / count / 2))

def BadTerms(minRassAndInd, maxRass):
    for el in minRassAndInd:
        if el[0] > maxRass:
            return True
    return False

def FindIndWithMaxRass(cluster, elems):
    result = []
    for el in elems:
        result.append(Evkl(el, cluster))
    return numpy.argmax(result)

def Solution(boolRandom = False):
    Nclusters = GetMatrix("fruits-and-vegetables-train.csv")
    # Тут хранятся координаты центров кластеров
    clusters = []
    # Инициализация
    if boolRandom:
        clusters.append(Nclusters[0])
        Nclusters.pop(0)
    else:
        temp = random.randrange(0, len(Nclusters))
        clusters.append(Nclusters[temp])
        Nclusters.pop(temp)

    # Находим самый далёкий элемент - наш второй кластер
    index = FindIndWithMaxRass(clusters[0], Nclusters)
    clusters.append(Nclusters[index])
    Nclusters.pop(index)

    # Находим минимальные расстояния до кластеров для каждого элемента
    minRassAndIndCl = []
    for i in range(0, len(Nclusters)):
        minRass = math.inf
        minInd = -1
        for j in range(0, len(clusters)):
            rass = Evkl(Nclusters[i], clusters[j])
            if rass < minRass:
                minRass = rass
                minInd = j
        minRassAndIndCl.append([minRass, minInd])

    print('Точки, выбранные за центры кластеров')
    for row in clusters:
        print(row)
    print('')
    iter = 1

    while BadTerms(minRassAndIndCl, MaxRass(clusters)):
        print('Итерация №', iter)
        iter = iter + 1
        # Найдём далёкую точку и переведём её в кластеры
        indNewCl = -1
        maxRass = -math.inf
        for i in range(0, len(minRassAndIndCl)):
            if maxRass < minRassAndIndCl[i][0]:
                maxRass = minRassAndIndCl[i][0]
                indNewCl = i
        print('Для нашего порога = ', MaxRass(clusters), ' нашлась точка удалённая на ', minRassAndIndCl[indNewCl][0])
        clusters.append(Nclusters[indNewCl])
        Nclusters.pop(indNewCl)
        # Перезапишем расстояния до кластеров
        minRassAndIndCl = []
        for i in range(0, len(Nclusters)):
            minRass = math.inf
            minInd = -1
            for j in range(0, len(clusters)):
                rass = Evkl(Nclusters[i], clusters[j])
                if rass < minRass:
                    minRass = rass
                    minInd = j
            minRassAndIndCl.append([minRass, minInd])
    print('Количество кластеров = ', len(clusters))

    color = ['red', 'blue', 'green', 'yellow', 'orange', 'pink', 'c', 'black', 'brown']
    pca = PCA(n_components=3)
    fig = plot.figure()
    ax = fig.add_subplot(111, projection='3d')
    clusters = pca.fit_transform(clusters)
    for i in range(0, len(clusters)):
        ax.scatter(clusters[i][0], clusters[i][1], clusters[i][2], color=color[i], marker="x", s=100)
        group = []
        for j in range(0, len(Nclusters)):
            if i == minRassAndIndCl[j][1]:
                group.append(Nclusters[j])
        if len(group) > 0:
            if len(group) == 1:
                group.append(group[0])
            group = pca.transform(group)
            for j in range(0, len(group)):
                ax.scatter(group[j, 0], group[j, 1], group[j, 2], color=color[i], s=30)
    plot.show()


Solution(False)
#Solution()