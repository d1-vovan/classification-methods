import csv
import math
import random
import numpy
import matplotlib.pyplot as plot
from sklearn.decomposition import PCA

def Evkl(vx, vy):
    # Метрика Евклида
    sum = 0
    for k in range(len(vx)):
        sum = sum + (vx[k] - vy[k]) ** 2
    return float('{:.2f}'.format(math.sqrt(sum)))

def GetFullMatrix (name):
    results = []
    with open(name, newline='') as File:
        reader = csv.reader(File)
        for row in reader:
            results.append(row)
    results.pop(0)
    return results

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
def GetFullMatrix (name):
    results = []
    with open(name, newline='') as File:
        reader = csv.reader(File)
        for row in reader:
            results.append(row)
    results.pop(0)
    return results

def GetMinIndex(el, clusters):
    result = []
    for cluster in clusters:
        result.append(Evkl(el, cluster))
    return numpy.argmin(result)

def GetNewCenter(indexC, indElInCl, data):
    count = 0
    sum = [0]*len(data[0])

    for i in range(0, len(data)):
        if indexC == indElInCl[i]:
            for j in range(0, len(data[i])):
                sum[j] = sum[j] + data[i][j]
            count = count + 1
    for i in range(0, len(data[i])):
        sum[i] = float('{:.2f}'.format(sum[i] / count))
    return sum

def isEndCycle(oldC, newC):
    for i in range(0, len(oldC)):
        if oldC[i] != newC[i]:
            return False
    return True

def Solution(number = 1, boolRandom = False):
    if number < 1:
        print('Нужен минимум 1 кластер')
        return
    data = GetMatrix("fruits-and-vegetables-train.csv")
    # Тут хранятся координаты центров кластеров
    center_k = []
    newCenter_k = []
    # Инициализация
    if boolRandom:
        center_k = data[0:number]
    else:
        temp = list(range(0, len(data)))
        temp = random.sample(temp, number)
        for i in temp:
            center_k.append(data[i])
    print('Точки, выбранные за центры кластеров')
    for row in center_k:
        print(row)
    print('')
    iter = 0
    indexCluster = []

    # Проверка на полное совпадение предыдущего и нынешнего шага
    while center_k != newCenter_k:
        iter = iter + 1
        print('Итерация №', iter)
        if len(newCenter_k) > 0:
            for i in range(0, number):
                center_k[i] = newCenter_k[i]

        # Тут для каждого элемента хранится кластер, к которому он принадлежит
        indexCluster = []
        for el in data:
            indexCluster.append(GetMinIndex(el, center_k))

        # Обновление центров
        newCenter_k = []
        for i in range(0, number):
            newCenter_k.append(GetNewCenter(i, indexCluster, data))
        print('Старые координаты центров кластеров: ', center_k)
        print('Новые координаты центров кластеров: ', newCenter_k)

    print('')
    print('Метод сошёлся. Координаты центров кластеров:')
    for row in center_k:
        print(row)

    full_mat = GetFullMatrix("fruits-and-vegetables-train.csv")
    for i in range(len(center_k)):
        print('Кластер №', i)
        for j in range(len(indexCluster)):
            if indexCluster[j] == i:
                print(full_mat[j][0], ' + ', full_mat[j])

    color = ['red', 'blue', 'green', 'yellow', 'orange', 'pink', 'c', 'black', 'brown']
    pca = PCA(n_components=3)
    fig = plot.figure()
    ax = fig.add_subplot(111, projection='3d')
    temp = len(center_k)
    if temp == 1:
        center_k.append(center_k[0])
        center_k.append(center_k[0])
    if temp == 2:
        center_k.append(center_k[1])
    center_k = pca.fit_transform(center_k)
    data = pca.transform(data)
    for i in range(temp):
        ax.scatter(center_k[i][0], center_k[i][1], center_k[i][2], color=color[i], marker="x", s=100)
        for j in range(len(data)):
            if indexCluster[j] == i:
                ax.scatter(data[j, 0], data[j, 1], data[j, 2], color=color[i], s=30)
    plot.show()




# Тут можно выбрать запустить метод k-means. Первый параметр - количество кластеров, второй - рандомная ли генерация.
# Не более 9-ти
Solution(4)