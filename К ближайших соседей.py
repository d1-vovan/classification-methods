import csv
import math



def Evkl(vx, vy):
    # Метрика Евклида
    sum = 0
    for k in range(len(vx)):
        sum = sum + (float(vx[k].replace(',', '.')) - float(vy[k].replace(',', '.'))) ** 2
    return math.sqrt(sum)

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
    return results
def GetFullMatrix (name):
    results = []
    with open(name, newline='') as File:
        reader = csv.reader(File)
        for row in reader:
            results.append(row)
    results.pop(0)
    return results

def Solution(number = 1):
    train = GetMatrix("fruits-and-vegetables-train.csv")
    test = GetMatrix("fruits-and-vegetables-test.csv")
    full_train = GetFullMatrix("fruits-and-vegetables-train.csv")
    full_test = GetFullMatrix("fruits-and-vegetables-test.csv")

    for i in range(0, len(test)):
        all_answer = []
        for j in range(0, len(train)):
            all_answer.append([Evkl(test[i], train[j]), full_train[j][10]])
        all_answer.sort()
        all_answer = all_answer[0:number]

        fruits = 0
        vegetables = 0
        for j in range(0, number):
            if all_answer[j][1] == "fruit":
                fruits = fruits + 1
            else:
                vegetables = vegetables + 1
        # Вывод результата
        if fruits > vegetables:
            print('Продукт ', full_test[i], ' оказался fruit.      Результаты fruit | vegetable = ', fruits, ' | ',  vegetables)
        else:
            print('Продукт ', full_test[i], ' оказался vegetables.      Результаты fruit | vegetable =', fruits, ' | ', vegetables)



# Тут можно выбрать различное количество ближайщих соседей к элементу

Solution(8)