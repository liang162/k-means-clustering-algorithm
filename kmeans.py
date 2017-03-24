import sys
import csv
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

#data array
data = []

#temp
temp = []

#the array that filtered out useless information
result = []

#a list of k random numbers
random_list = []

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
    random_list.append(int(random.random() * 21090))

for i in range(0, int(numOfClusters)):
    print "Centroid" + str(i + 1) + "=[" + str(result[0][random_list[i]]) + "," + str(result[1][random_list[i]]) + "," + str(result[2][random_list[i]]) + "," + str(result[3][random_list[i]]) + "]"



