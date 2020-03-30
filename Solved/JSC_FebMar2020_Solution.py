
from random import uniform
import numpy as np
import matplotlib.pyplot as plt


def crosses_one_gridline(x0,y0,d,theta):
	# assumes both x0 and y0 are between 0 and 1
	# assumes theta lies between 0 and pi/2
	# assumes d < sqrt(2)

	num_x_cross = np.floor(x0 + d * np.cos(theta)) # either 0 or 1
	num_y_cross = np.floor(y0 + d * np.sin(theta)) # either 0 or 1

	return num_x_cross + num_y_cross == 1


for experiment in range(1):
	
	##############################

	# SIMULATION PARAMETERS
	step = 0.01
	n_samples = 10000
	d_values = np.round(np.arange(0.8, np.sqrt(2), step), 10)

	##############################

	# INITIALIZATIONS
	probabilities = []
	optimal_distance = 0
	optimal_prob = 0

	##############################

	for d in d_values:
		n_single_crosses = 0

		for i in range(n_samples):
			x0 = uniform(0, 1)
			y0 = uniform(0, 1)
			theta = uniform(0, 1) * np.pi / 2 # selection theta between 0 and pi/2 at random

			if crosses_one_gridline(x0, y0, d, theta):
				n_single_crosses += 1


		prob = n_single_crosses / n_samples

		probabilities.append(prob)

		if prob > optimal_prob:
			optimal_prob = prob
			optimal_distance = d



	print("experiment #:", experiment)
	print("optimal distance:", optimal_distance)
	print("optimal prob:", optimal_prob)
	print()

	plt.plot(d_values, probabilities)
	plt.show()
	

