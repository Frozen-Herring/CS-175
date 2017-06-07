import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

avgEpisodesArray = []
nArray = []
alphaArray = []
gammaArray = []


for i, line in enumerate(open("C:/Users/Admin/Desktop/optimization results justin.csv")):
    if i != 0:
        split = line.split("\t")

        avgEpisodesArray.append(split[0])
        nArray.append(split[1])
        alphaArray.append(split[2])
        gammaArray.append(split[3])


xYPairToZDict = defaultdict(list)
for x,y,z in zip(alphaArray, gammaArray, avgEpisodesArray):
    xYPairToZDict[(x,y)].append(float(z))

x, y, z = [], [], []

for key in xYPairToZDict.keys():
    x.append(key[0])
    y.append(key[1])
    z.append(sum(xYPairToZDict.get(key)))

for i in range(len(x)):
    print "x="+str(x[i]) + ", y="+str(y[i]) + ", z="+str(z[i])


x = np.array(x)
y = np.array(y)
z = np.array(z)

xstr = "alpha value"
ystr = "gamma value"
zstr = "episodes to finish"



plt.scatter(x,y,c=z,s=500, alpha=1)
plt.xlabel(xstr)
plt.ylabel(ystr)
plt.title("grayscale = " + zstr)
plt.gray()
print(z)
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
