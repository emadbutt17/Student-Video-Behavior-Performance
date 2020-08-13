from problem1 import *
from problem2 import *
from problem3 import *
import sklearn

def obtainTxt(file):
    f = open(file, 'r')
    with f as File:
        full_data = [line.split() for line in File]
    
    col_names = full_data[0]
    data = full_data[1:]

    f.close()
    return col_names, data

def find_range(data):
    fracSpent = 2
    fracComp = 3
    fracPaused = 5
    numPauses = 6
    avgPBR = 7
    numRWs = 9
    numFFs = 10 # 7 features

    range_data_min = []
    range_data_max = []
    new_data = [float(data[0][fracSpent]), float(data[0][fracComp]), float(data[0][fracPaused]), float(data[0][numPauses]), float(data[0][avgPBR]), float(data[0][numRWs]), float(data[0][numFFs])]
    range_data_min = new_data
    range_data_max = new_data.copy()
    for row in data:
        if (float(row[fracSpent]) < range_data_min[0]): range_data_min[0] = float(row[fracSpent])
        elif (float(row[fracSpent]) > range_data_max[0]): range_data_max[0] = float(row[fracSpent])

        if (float(row[fracComp]) < range_data_min[1]): range_data_min[1] = float(row[fracComp])
        elif (float(row[fracComp]) > range_data_max[1]): range_data_max[1] = float(row[fracComp])

        if (float(row[fracPaused]) < range_data_min[2]): range_data_min[2] = float(row[fracPaused])
        elif (float(row[fracPaused]) > range_data_max[2]): range_data_max[2] = float(row[fracPaused])

        if (float(row[numPauses]) < range_data_min[3]): range_data_min[3] = float(row[numPauses])
        elif (float(row[numPauses]) > range_data_max[3]): range_data_max[3] = float(row[numPauses])

        if (float(row[avgPBR]) < range_data_min[4]): range_data_min[4] = float(row[avgPBR])
        elif (float(row[avgPBR]) > range_data_max[4]): range_data_max[4] = float(row[avgPBR])

        if (float(row[numRWs]) < range_data_min[5]): range_data_min[5] = float(row[numRWs])
        elif (float(row[numRWs]) > range_data_max[5]): range_data_max[5] = float(row[numRWs])

        if (float(row[numFFs]) < range_data_min[6]): range_data_min[6] = float(row[numFFs])
        elif (float(row[numFFs]) > range_data_max[6]): range_data_max[6] = float(row[numFFs])

    return range_data_min, range_data_max
    
if __name__ == '__main__' :
    path = 'behavior-performance.txt'
    col_names, data = obtainTxt(path)

    problem1(data)
    # problem2(data)
    # problem3(data)
    # print('sklearn: %s', sklearn.__version__)
    # range_data_min, range_data_max = find_range(data)
    # print("Min values of: ", range_data_min)
    # print("Max values of: ", range_data_max)
    
    
    
