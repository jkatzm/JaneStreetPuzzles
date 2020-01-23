import numpy as np
from scipy.ndimage.measurements import label

################################################################
# Utility Functions
################################################################

def get_row(grid, i):
	return grid[i,:]

def get_column(grid, j):
	return grid[:,j]


def partitions(n, k, l=1):
	# n is the integer to partition, k is the number of parts, l is the min element size
	if k < 1:
	    raise StopIteration

	if k == 1:
	    if l <= n <= 7:
	        yield (n,)
	    raise StopIteration

	for i in range(l, 8):
	    for result in partitions(n-i, k-1, i):
	        yield result + (i,)

def illegal_partition(grid, partition):
	counts = {i : (grid==i).sum() for i in range(1,8)}

	for part in partition:
		counts[part] += 1

	return any([counts[i] > i for i in range(1,8)])

def legal_row_partitions(grid, i):
	row = get_row(grid, i)
	n = 20 - sum(row)
	k = 4 - np.count_nonzero(row)
	return [p for p in partitions(n, k) if not illegal_partition(grid, p)]

def legal_col_partitions(grid, j):
	col = get_column(grid, j)
	n = 20 - sum(col)
	k = 4 - np.count_nonzero(col)
	return [p for p in partitions(n, k) if not illegal_partition(grid, p)]

################################################################
# Secondary Driver Programs
################################################################

def forceable_rows(grid):
	indices = {}

	for i in range(7):
		current_row = get_row(grid, i)
		n_nonzero = np.count_nonzero(current_row)

		if n_nonzero == 3:
			return { i : 20 - sum(current_row) }

		elif n_nonzero == 2:
			if (sum(current_row) == 6) | (sum(current_row) == 7): # forces 7,7 and 7,6 respectively
				return { i : 7 }

			legal_p = legal_row_partitions(grid, i)
			if len(legal_p) == 1:
				if len(set(legal_p[0])) == 1:
					indices[i] = legal_p[0][0]

	return indices

def forceable_cols(grid):
	indices = {}

	for j in range(7):
		current_col = get_column(grid, j)
		n_nonzero = np.count_nonzero(current_col)

		if n_nonzero == 3:
			return { j : 20 - sum(current_col) }

		elif n_nonzero == 2:
			if (sum(current_col) == 6) | (sum(current_col) == 7): # forces 7,7 and 7,6 respectively
				return { j : 7 }

			legal_p = legal_col_partitions(grid, j)
			if len(legal_p) == 1:
				if len(set(legal_p[0])) == 1:
					indices[j] = legal_p[0][0]

	return indices

def force_rows(grid, index_value_map):
	for i,value in index_value_map.items():
		for j in range(7):
			if grid[i][j] == 0:
				grid[i][j] = value
				if valid_placement(grid, i, j):
					solve_puzzle(grid)
				grid[i][j] = 0

def force_cols(grid, index_value_map):
	for j,value in index_value_map.items():
		for i in range(7):
			if grid[i][j] == 0:
				grid[i][j] = value
				if valid_placement(grid, i, j):
					solve_puzzle(grid)
				grid[i][j] = 0

################################################################
# Constraint Checking
################################################################

def valid_placement(grid, i, j):
	if (grid[i][j] > 7) | (grid[i][j] < 1):
		return False

	if (grid == grid[i][j]).sum() > grid[i][j]:
		return False

	row = get_row(grid, i)

	if sum(row) > 20:
		return False

	elif (sum(row) == 20) & (np.count_nonzero(row) != 4):
		return False

	elif (sum(row) < 20) & (np.count_nonzero(row) >= 4):
		return False

	col = get_column(grid, j)

	if sum(col) > 20:
		return False

	elif (sum(col) == 20) & (np.count_nonzero(col) != 4):
		return False

	elif (sum(col) < 20) & (np.count_nonzero(col) >= 4):
		return False

	return True

def valid_subgrids(final_grid):
	for i in range(6):
		for j in range(6):
			if (final_grid[i:i+2, j:j+2] == 0).sum() == 0:
				return False
	return True

def valid_rows_cols_counts(final_grid):
	for n in range(7):
		if (sum(get_row(final_grid, n)) != 20) | (np.count_nonzero(get_row(final_grid, n)) != 4):
			return False

		if (sum(get_column(final_grid, n)) != 20) | (np.count_nonzero(get_column(final_grid, n)) != 4):
			return False

		if (final_grid == n+1).sum() != n+1:
			return False

	return True

def valid_connectivity(final_grid):
	labeled_array, num_features = label(final_grid != 0)
	return num_features == 1

################################################################
# Primary Driver Program
################################################################

def solve_puzzle(grid):
	fr = forceable_rows(grid)
	if len(fr) != 0:
		force_rows(grid, fr)
		return

	fc = forceable_cols(grid)
	if len(fc) != 0:
		force_cols(grid, fc)
		return

	if valid_subgrids(grid):
		if valid_rows_cols_counts(grid):
			if valid_connectivity(grid):
				print("solved!!!", '\n', grid)
				exit()
	return

################################################################
################################################################
################################################################

JaneStreetGrid = np.array([
	[0,4,0,0,0,0,0],
	[0,0,6,3,0,0,6],
	[0,0,0,0,0,5,5],
	[0,0,0,4,0,0,0],
	[4,7,0,0,0,0,0],
	[2,0,0,7,4,0,0],
	[0,0,0,0,0,1,0]
])

print(JaneStreetGrid, '\n')

solve_puzzle(JaneStreetGrid)



