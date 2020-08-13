import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn import metrics


def obtain_logistic_data_p3(data):
    fracSpent = 2
    fracComp = 3
    fracPaused = 5
    numPauses = 6
    avgPBR = 7
    numRWs = 9
    numFFs = 10 # 7 features
    avg_score = 11 # 1 score (output)

    log_data = [[float(row[fracSpent]), float(row[fracComp]), float(row[fracPaused]), float(row[numPauses]), float(row[avgPBR]), float(row[numRWs]), float(row[numFFs])] for row in data]
    output = [int(row[avg_score]) for row in data]
    return log_data, output


def train_test_split2(X, y):
    X_train = []
    y_train = []
    X_test = []
    y_test = []

    listOftrainSlices = [[slice(5860,29304)], [slice(0,5860),slice(11720,29304)], [slice(0,11720),slice(17580,29304)], [slice(0,17580),slice(23440,29304)], [slice(0,23440)]]
    listOftestSlices = [slice(0,5860), slice(5860,11720), slice(11720,17580), slice(17580,23440), slice(23440,29304)]

    for i in range(len(listOftestSlices)):
        train_slice = listOftrainSlices[i]
        test_slice = listOftestSlices[i]

        if (len(train_slice) == 1):
            X_train.append(X[train_slice[0]])
            y_train.append(y[train_slice[0]])

        else:
            X_train.append(X[train_slice[0]] + X[train_slice[1]])
            y_train.append(y[train_slice[0]] + y[train_slice[1]])

        X_test.append(X[test_slice])
        y_test.append(y[test_slice])

    return X_train, y_train, X_test, y_test

def Ind_Accuracy(X_train, y_train, X_test, y_test, c):
    logreg = LogisticRegression(solver='lbfgs', class_weight='balanced', C=c)
    # print("Prio reshape:", X_train[0:10])
    X_train_reshap = np.array(X_train)
    X_train_reshap.reshape((1,-1))
    # print("Post reshape:", X_train_reshap[0:10])
    # return 1
    logreg.fit(X_train, y_train)
    y_pred = logreg.predict(X_test)
    return metrics.accuracy_score(y_test, y_pred)

def ObtainAccuracy(X_train, y_train, X_test, y_test, c):
    accuracy_score = []
    for i in range(len(X_train)): # iterate 5 times for 5-fold
        accuracy_score.append(Ind_Accuracy(X_train[i], y_train[i], X_test[i], y_test[i], c))

    return sum(accuracy_score) / 5

def Logistic_Regression(data,output):
    total_accuracy_score = []
    C_total = np.logspace(-1, 1.5, num=15)

    X_train, y_train, X_test, y_test = train_test_split2(data, output)

    for C in C_total:
        accuracy_score = ObtainAccuracy(X_train, y_train, X_test, y_test, C)
        total_accuracy_score.append(accuracy_score)

    plt.plot(C_total, total_accuracy_score)
    plt.xlabel("C Values")
    plt.ylabel("Accuracy Score")
    plt.title("Accuracy of In-Video Quiz Question")
    plt.show()
    # print(total_accuracy_score)
    max_acc_index = np.argmax(total_accuracy_score)
    print("Maximum accuracy: ", max(total_accuracy_score))
    print("Corresponding C value: ", C_total[max_acc_index])
    
    return



def problem3(data):
    log_data, output = obtain_logistic_data_p3(data)
    Logistic_Regression(log_data, output)
    # Linear_Regression(X, y)
    # print(len(log_data))