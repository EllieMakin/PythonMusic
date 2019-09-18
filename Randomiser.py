import random

points = 10
limit = 72
mean = 5
standardDistribution = 5
for i in range(points):
    print random.normalvariate(mean, standardDistribution)
