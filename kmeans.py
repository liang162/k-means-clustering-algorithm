import sys
import csv
import math
import random
import numpy as np
import matplotlib.pyplot as plt

#notes
#3: latitude, 0 in result
#4: longitude, 1 in result
#6: reviewCount, 2 in result
#7: checkins, 3 in result

#setting up, reading the parameter
dataFilename = sys.argv[1]
numOfClusters = sys.argv[2]
clusteringOption = sys.argv[3]
plotOption = sys.argv[4]

#data array, len(data) = 21092
data = []

#temp
temp = []

#the array that filtered out useless information
result = []

#a list of k random numbers
centroid_list = []

#a list of cluster list
cluster_list = []

#initialize cluster list
for i in range(0, int(numOfClusters)):
    temp_cluster_list = []
    cluster_list.append(temp_cluster_list)

#open csv file
with open(dataFilename) as csvfile:
    temp_data = csv.reader(csvfile, delimiter=',')
    for row in temp_data:
        data.append(row)

#take transpose
if(int(clusteringOption) == 5):
    for i in range(0, 19):
        if(i == 3 or i == 4 or i == 6 or i == 7):
            for j in range(1, int(len(data) * 0.03)):
                if(data[int(len(data) * random.random())][i] == "latitude" or data[int(len(data) * random.random())][i] == "reviewCount" or data[int(len(data) * random.random())][i] == "longitude" or data[int(len(data) * random.random())][i] == "checkins"):
                    continue
                else:
                    temp.append(float(data[int(len(data) * random.random())][i]))
            result.append(temp)
            temp = []
else:
    for i in range(0, 19):
        if(i == 3 or i == 4 or i == 6 or i == 7):
            for j in range(1, len(data)):
                temp.append(float(data[j][i]))
            result.append(temp)
            temp = []

if(int(clusteringOption) == 2):
    for i in range(0, len(data) - 1):
        result[2][i] = math.log(float(result[2][i]))
        result[3][i] = math.log(float(result[3][i]))
elif(int(clusteringOption) == 3):
    for i in range(0, 4):
        standard_dev = np.std(result[i])
        mean = np.mean(result[i])
        for j in range(0, len(data) - 1):
            result[i][j] = (result[i][j] - mean) / standard_dev

#generate a random list, initial centroid
for i in range(0, int(numOfClusters)):
    if(int(clusteringOption) == 5):
        centroid_list.append(int(random.random() * (len(data) - 1) * 0.03))
    else:
        centroid_list.append(int(random.random() * (len(data) - 1)))

#modify centroid_list to be [[33.65, -111.45, 22, 94], [33.65, -111.45, 22, 94], [33.65, -111.45, 22, 94]]
for i in range(0, int(numOfClusters)):
    temp_centroid_list = []
    for j in range(0, 4):
        temp_centroid_list.append(float(result[j][centroid_list[i]]))
    centroid_list[i] = temp_centroid_list
    temp_centroid_list = []

change = 1
distance_list = []
temp_storage_of_cluster_list = [-1] * (len(data) - 1)
#need to rerun
need_to_rerun = 0

if(int(clusteringOption) == 5):
    maximum = int((len(data) - 1) * 0.03) - 2
else:
    maximum = len(data) - 1

while True:
    need_to_rerun = 0
    for i in range(0, maximum):
        for j in range(0, int(numOfClusters)):
            if(int(clusteringOption) == 4):
                distance_list.append(abs(float(result[0][i]) - float(centroid_list[j][0])) + abs(float(result[1][i]) - float(centroid_list[j][1])) + abs(float(result[2][i]) - float(centroid_list[j][2])) + abs(float(result[3][i]) - float(centroid_list[j][3])))
            else:
                distance_list.append(math.sqrt((float(result[0][i]) - float(centroid_list[j][0]))**2 + (float(result[1][i]) - float(centroid_list[j][1]))**2 + (float(result[2][i]) - float(centroid_list[j][2]))**2 + (float(result[3][i]) - float(centroid_list[j][3]))**2))
        index_of_min = distance_list.index(min(distance_list))

        if(temp_storage_of_cluster_list[i] != index_of_min):
            need_to_rerun = need_to_rerun + 1
        #assign cluster to list
        temp_storage_of_cluster_list[i] = index_of_min
        cluster_list[index_of_min].append(i)
        distance_list = []

    #get the new centroid list, method: look for the shortest distance sum
    new_centroid_list = []
    for k in range(0, int(numOfClusters)):
        temp_new_centroid_list = []
        for l in range(0, 4):
            total = 0.0
            average = 0.0
            for m in range(0, len(cluster_list[k])):
                total = total + float(result[l][cluster_list[k][m]])
            if(len(cluster_list[k]) == 0):
                average = 0
            else:
                average = total / len(cluster_list[k])
            temp_new_centroid_list.append(average)
        new_centroid_list.append(temp_new_centroid_list)
        temp_new_centroid_list = []
    centroid_list = new_centroid_list
    
    if(need_to_rerun < 0.001 * len(data) - 1):
        break

#WC-SSE
WC_SSE = 0
for i in range(0, int(numOfClusters)):
    temp_WC_SSE = 0
    for j in range(0, len(cluster_list[i])):
        temp_WC_SSE = temp_WC_SSE + (float(result[0][cluster_list[i][j]]) - float(centroid_list[i][0]))**2 + (float(result[1][cluster_list[i][j]]) - float(centroid_list[i][1]))**2 + (float(result[2][cluster_list[i][j]]) - float(centroid_list[i][2]))**2 + (float(result[3][cluster_list[i][j]]) - float(centroid_list[i][3]))**2
    WC_SSE = WC_SSE + temp_WC_SSE

print "WC-SSE=" + str(WC_SSE)

#prints centroids
for i in range(0, int(numOfClusters)):
    print "Centroid" + str(i + 1) + "=[" + str(centroid_list[i][0]) + "," + str(centroid_list[i][1]) + "," + str(centroid_list[i][2]) + "," + str(centroid_list[i][3]) + "]"

#plot options
if(plotOption == "no"):
    ahfiaegfu = 0
elif(int(plotOption) == 1):
    #plot latitude and longitude
    for i in range(0, int(numOfClusters)):
        latitude_x = []
        longitude_y = []
        color = (random.random(), random.random(), random.random())
        for j in range(0, len(cluster_list[i])):
            latitude_x.append(result[0][cluster_list[i][j]])
            longitude_y.append(result[1][cluster_list[i][j]])
        plt.scatter(latitude_x, longitude_y, c=color)

    plt.show()
elif(int(plotOption) == 2):
    #plot latitude and longitude
    for i in range(0, int(numOfClusters)):
        latitude_x = []
        longitude_y = []
        color = (random.random(), random.random(), random.random())
        for j in range(0, len(cluster_list[i])):
            latitude_x.append(result[2][cluster_list[i][j]])
            longitude_y.append(result[3][cluster_list[i][j]])
        plt.scatter(latitude_x, longitude_y, c=color)

    plt.show()

#done




