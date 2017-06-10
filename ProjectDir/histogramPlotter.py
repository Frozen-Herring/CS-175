import numpy as np
import scipy.stats as stats
import pylab as plt

h = sorted(
    [86, 100, 119, 80, 79, 148, 115, 138, 68, 158, 73, 153, 168, 220, 90, 89, 116, 148, 66, 95, 136, 210, 119, 88, 91,
     140, 101, 79, 145, 3099, 87, 98, 257, 93, 441, 151, 2679, 80, 74, 145, 100, 85, 204, 108, 84, 3146, 91, 112, 74,
     88, 73, 97, 121, 76, 89, 132, 70, 171, 72, 69, 128, 104, 93, 93, 84, 94, 217, 106, 119, 78, 66, 97, 83, 58, 93,
     230, 86, 158, 80, 359, 362, 111, 77, 110, 103, 184, 94, 101, 85, 128, 82, 89, 102, 94, 84, 100, 96, 79, 202, 210])

#remove 3099, 2679, 3146
# h = sorted(
#     [86, 100, 119, 80, 79, 148, 115, 138, 68, 158, 73, 153, 168, 220, 90, 89, 116, 148, 66, 95, 136, 210, 119, 88, 91,
#      140, 101, 79, 145, 87, 98, 257, 93, 441, 151, 80, 74, 145, 100, 85, 204, 108, 84, 91, 112, 74,
#      88, 73, 97, 121, 76, 89, 132, 70, 171, 72, 69, 128, 104, 93, 93, 84, 94, 217, 106, 119, 78, 66, 97, 83, 58, 93,
#      230, 86, 158, 80, 359, 362, 111, 77, 110, 103, 184, 94, 101, 85, 128, 82, 89, 102, 94, 84, 100, 96, 79, 202, 210])

for i in (range(7)):
    fit = stats.norm.pdf(h, np.mean(h), np.std(h))  # this is a fitting indeed

    plt.plot(h, fit, '-o')
    plt.title("Distribution of all 100 z values (number of episodes to finish the maze)\nwhere x=alpha=.8, y=gamma=.8");
    plt.xlabel("The " + str(i) + " highest values have been removed\nMean = " + str(np.mean(h)))

    plt.hist(h, normed=True)  # use this to draw histogram of your data

    plt.show()  # use may also need add this
    plt.clf()
    h.remove(h[-1])
