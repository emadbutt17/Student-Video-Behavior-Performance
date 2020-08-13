import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

def reduced_data_p2(data):
    all_users = [i[0] for i in data]
    all_users_sets = set(all_users)
    count_videos = dict.fromkeys(all_users_sets, 0)

    for user in data:
        count_videos[user[0]] += 1
    delete_users = []
    for key, value in count_videos.items():
        if value < 47: # 47 is the threshold for at least half of your quizzes
          delete_users.append(key)

    for key in delete_users:
        del count_videos[key] 

    return count_videos # Total of 94 elements

def obtain_regression_data_p2(data, valid_users):
    listOfPoints = []
    userID = 0 # 1 user id (key)
    fracSpent = 2
    fracComp = 3
    fracPaused = 5
    numPauses = 6
    avgPBR = 7
    numRWs = 9
    numFFs = 10 # 7 features
    avg_score = 11 # 1 score (output)
    all_features = dict.fromkeys(valid_users.keys(), []) # create a dictionary where the keys are the same as the valid users and values are empty lists


    for row in data:
        if row[0] in valid_users: 
            attribute_list = [float(row[fracSpent]), float(row[fracComp]), float(row[fracPaused]), float(row[numPauses]), float(row[avgPBR]), float(row[numRWs]), float(row[numFFs]), float(row[avg_score])] # current attributes in data table
        
            current_list = all_features[row[userID]]
            if len(current_list) == 0: # first userID that I encounter, simply append that list
                all_features[row[userID]] = all_features[row[userID]] + attribute_list # Attribute_list will be the new list

            else: # otherwise, add each element to that list
                for i in range(len(current_list)):
                    current_list[i] += attribute_list[i]

    for key, value in all_features.items():
        num_vids = valid_users[key] # number of videos for a student
        total_list = [i / num_vids for i in value] # divide by the total number of videos
        listOfPoints.append(total_list) # add this to the list of points for the clustering algorithm

    X = [point[0:7] for point in listOfPoints]
    y = [point[-1] for point in listOfPoints]

    return X,y


def train_test_split(X,y):
    X_train = []
    y_train = []
    X_test = []
    y_test = []

    listOftrainSlices = [[slice(19,94)], [slice(0,19),slice(38,94)], [slice(0,38),slice(57,94)], [slice(0,57),slice(76,94)], [slice(0,76)]]
    listOftestSlices = [slice(0,19), slice(19,38), slice(38,57), slice(57,76), slice(76,94)] # remember that the final index must be 93, not 94

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

def Ind_MSE(X_train, y_train, X_test, y_test, l):
    mean_X = np.mean(X_train, axis=0) # normalize the data
    std_X = np.std(X_train, axis=0)
    mean_y = np.mean(y_train)
    std_y = np.std(y_train)
    X_train_norm = (X_train - mean_X) / std_X
    y_train_norm = (y_train - mean_y) / std_y
    X_test_norm = (X_test - mean_X) / std_X

    regr = Ridge(alpha=l, fit_intercept=True)
    regr.fit(X_train_norm,y_train_norm) # fit the model with normalized data
    y_pred_train_norm = regr.predict(X_train_norm)
    y_pred_train = (y_pred_train_norm * std_y) + mean_y
    y_pred_test_norm = regr.predict(X_test_norm) # predict the data for the testing data
    y_pred_test = (y_pred_test_norm * std_y) + mean_y # Unnormalize y after prediction

    train_MSE = mean_squared_error(y_train, y_pred_train)
    test_MSE = mean_squared_error(y_test, y_pred_test)

    return train_MSE, test_MSE

def ObtainMSEs(X_train, y_train, X_test, y_test, l):
    train_MSE = []
    test_MSE = []
    for i in range(len(X_train)):
        train_MSE_ind, test_MSE_ind = Ind_MSE(X_train[i], y_train[i], X_test[i], y_test[i], l)
        train_MSE.append(train_MSE_ind)
        test_MSE.append(test_MSE_ind)
    return sum(train_MSE) / len(train_MSE), sum(test_MSE) / len(test_MSE)


def Linear_Regression(X, y):
    total_train_MSE = []
    total_test_MSE = []
    lambda_range = np.logspace(-1, 2.5, num=351)
    X_train, y_train, X_test, y_test = train_test_split(X, y) # return the split training and testing data where each is a list of five-fold

    for l in lambda_range:
        train_MSE_ind, test_MSE_ind = ObtainMSEs(X_train, y_train, X_test, y_test, l)
        total_train_MSE.append(train_MSE_ind)
        total_test_MSE.append(test_MSE_ind)

    # print(train_MSE_ind)
    # print(test_MSE_ind)
    
    fig, axs = plt.subplots(2)
    fig.suptitle("Comparison of MSE")
    axs[0].plot(lambda_range, total_train_MSE)
    axs[0].set_title("Average MSE for training data")
    axs[1].plot(lambda_range, total_test_MSE)
    axs[1].set_title("Average MSE for testing data")
    axs[1].set(xlabel="Lambda Values",ylabel="Mean Squared Error")
    for ax in axs.flat:
        ax.label_outer()
    plt.show()

    min_MSE_index = np.argmin(total_test_MSE)
    min_lambda_value = lambda_range[min_MSE_index]
    print("Minimum testing MSE: ", min(total_test_MSE))
    print("Corresponding lambda value: ", min_lambda_value)


def problem2(data):
    valid_users = reduced_data_p2(data) # reduce the data to only students who completed at least half of the quizzes
    X, y = obtain_regression_data_p2(data, valid_users) # obtain the features and output data for the linear regression problem
    Linear_Regression(X, y)
    
    