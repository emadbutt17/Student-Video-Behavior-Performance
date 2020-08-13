import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def reduced_data_p1(data):
# only include students that complate at least 5 of the videos, look for when a userID has 5 or more entries
# create a list (or a set) of all user ids
    all_users = [i[0] for i in data]
    all_users_sets = set(all_users)
# from this set, iterate through your data and whenever something matches, you update your dictionary of names
    count_videos = dict.fromkeys(all_users_sets, 0)
    for user in data:
        count_videos[user[0]] += 1 # increment the dictionary value


    delete_users = [] # keep track of users you want to remove
    for key, value in count_videos.items():
        if value < 5:
            delete_users.append(key)

    for key in delete_users:
        del count_videos[key] # remove user from the dictionary
    #print(count_videos)
    return count_videos

def obtain_cluster_data_p1(data, valid_users):
    listOfPoints = [] # list of lists where each sublist is a points
    userID = 0
    fracSpent = 2
    fracComp = 3
    fracPaused = 5
    numPauses = 6
    avgPBR = 7
    numRWs = 9
    numFFs = 10

    all_features = dict.fromkeys(valid_users.keys(), []) # create a dictionary where the keys are the same and values are empty lists

    for row in data:
        if row[0] in valid_users: 
            attribute_list = [float(row[fracSpent]), float(row[fracComp]), float(row[fracPaused]), float(row[numPauses]), float(row[avgPBR]), float(row[numRWs]), float(row[numFFs])] # current attributes in data table

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

    return listOfPoints

def MeanSqError(point1,point2):
    running_sum = 0
    for i in range(len(point1)):
        running_sum += (point1[i] - point2[i])**2
    return running_sum

def ind_clustering_p1(listOfPoints, k):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(listOfPoints)
    clust_cent = kmeans.cluster_centers_
    clust_label = kmeans.labels_
    # print(clust_cent)
    # print(clust_label)
    total_sum = 0

    for i in range(len(clust_label)):
        curr_point = listOfPoints[i]
        curr_label = clust_label[i]
        curr_cent = clust_cent[curr_label] # index into the lsit of cluster centers based on the label
        total_sum += MeanSqError(curr_point, curr_cent)

    # print(len(curr_point))
    
    return total_sum / len(listOfPoints) # return the mean squared error for a specific k value
        



def clustering_p1(listOfPoints):
    k_range = list(range(4,24))
    listOfSquaredDist = []
    
    for k in k_range:
        listOfSquaredDist.append(ind_clustering_p1(listOfPoints, k))

    plt.plot(k_range, listOfSquaredDist, marker = "X")
    plt.xticks(k_range)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Total Squared Error Between Points and Assigned Cluster')
    plt.title('Cluster Comparison for Video-Watching Behavior')
    plt.show()
    print("Distance for k=11: ", listOfSquaredDist[10])

    return



def problem1(data):
    valid_users = reduced_data_p1(data) # reduce the data to only user ids we want
    listOfPoints = obtain_cluster_data_p1(data, valid_users) # Lists of lists to represent data for clustering
    clustering_p1(listOfPoints)

    
    
    
    
