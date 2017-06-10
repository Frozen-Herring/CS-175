import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import seaborn as sns
import pandas as pd



avgEpisodesArray = []
nArray = []
alphaArray = []
gammaArray = []


for i, line in enumerate(open("C:/Users/Admin/Desktop/optimization results justin.csv")):
# for i, line in enumerate(open("C:/Users/Admin/Desktop/optimization results.csv")):
    if i != 0:
        split = line.split("\t")

        avgEpisodesArray.append(split[0])
        nArray.append(split[1])
        alphaArray.append(split[2])
        gammaArray.append(split[3])


masterArray = [alphaArray,gammaArray,nArray]
masterArrayNames = ['alpha','gamma','n']
grayscaleArray = avgEpisodesArray
# grayscaleName = 'average agent episodes to get all rewards and get to end block'
grayscaleName = 'average agent episodes to find shortest path to all rewards (no exit)'

for i in range(3):
    masterArray.append(masterArray.pop(0))
    masterArrayNames.append(masterArrayNames.pop(0))



    xYPairToZDictList = defaultdict(list)
    for x,y,z in zip(masterArray[0], masterArray[1], grayscaleArray):
        xYPairToZDictList[(x, y)].append(float(z))

    x, y, z = [], [], []


    xyPairToZDictSum = dict()

    for key in xYPairToZDictList.keys():
        x.append(key[0])
        y.append(key[1])
        z.append(sum(xYPairToZDictList.get(key)))
        xyPairToZDictSum[(key[0], key[1])] = sum(xYPairToZDictList.get(key))





    for i in range(len(x)):
        print "x="+str(x[i]) + ", y="+str(y[i]) + ", z="+str(z[i])


    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    maximum = max(xyPairToZDictSum, key=xyPairToZDictSum.get)
    minimum = min(xyPairToZDictSum, key=xyPairToZDictSum.get)
    figTextString = "max x,y = (" + str(maximum[0]) + ", " + maximum[1] +") with " + str(xyPairToZDictSum[maximum]) + " episodes" + "\nmin x,y = (" + str(minimum[0]) + ", " + minimum[1] +") with " + str(xyPairToZDictSum[minimum]) + " episodes";
    # infoText = "Because of the different " + masterArrayNames[2] + " values which are not being graphed:\n Each x,y pair has " + str(len(xYPairToZDictList[(x[0],y[0])])) + " " + grayscaleName + " values.\n which have been averaged to make a single value for each x,y pair."
    print "the " + str(len(xYPairToZDictList[(x[0],y[0])])) + " z values for each x,y pair have been averaged to make a single z value.\n hidden variable: " + masterArrayNames[2]

    plt.scatter(x,y,c=z,s=500, alpha=1)
    plt.xlabel(masterArrayNames[0])
    plt.ylabel(masterArrayNames[1])
    plt.title("grayscale = " + grayscaleName + "\n" + figTextString)


    plt.gray()
    # print(z)
    # plt.savefig("x="+masterArrayNames[0]+"_y="+masterArrayNames[1]+"_Derek_Optimizer_9161708779")
    plt.savefig("x="+masterArrayNames[0]+"_y="+masterArrayNames[1]+"_Justin_Optimizer_9161708779")
    plt.show()
    plt.clf()




#
# plt.scatter(x,y,c=z,s=500, alpha=.1)
# plt.xlabel(xstr)
# plt.ylabel(ystr)
# plt.title("grayscale = " + zstr)
# plt.gray()
# plt.show()
#
# plt.clf()
