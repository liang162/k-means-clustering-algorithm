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
for i in range(0, 19):
    if(i == 3 or i == 4 or i == 6 or i == 7):
        for j in range(1, len(data)):
            temp.append(data[j][i])
        result.append(temp)
        temp = []

#generate a random list, initial centroid
for i in range(0, int(numOfClusters)):
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
while True:
    for i in range(0, len(data) - 1):
        for j in range(0, int(numOfClusters)):
            distance_list.append(math.sqrt((float(result[0][i]) - float(centroid_list[j][0]))**2 + (float(result[1][i]) - float(centroid_list[j][1]))**2 + (float(result[2][i]) - float(centroid_list[j][2]))**2 + (float(result[3][i]) - float(centroid_list[j][3]))**2))
        index_of_min = distance_list.index(min(distance_list))
        cluster_list[index_of_min].append(i)
        distance_list = []

    #reassign centroid, if centroid does NOT change, then change = 0, break
    old_centroid_list = centroid_list
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
    if(abs(float(old_centroid_list[0][0]) - float(new_centroid_list[0][0])) <= 0.000000001):
        print "change = 0, break"
        break
    else:
        centroid_list = new_centroid_list
        print "centroid_list != new_centroid_list"

for i in range(0, int(numOfClusters)):
    print "Centroid" + str(i + 1) + "=[" + str(centroid_list[i][0]) + "," + str(centroid_list[i][1]) + "," + str(centroid_list[i][2]) + "," + str(centroid_list[i][3]) + "]"

