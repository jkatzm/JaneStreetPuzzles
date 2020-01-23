import numpy as np

def get_row(board, i):
	return board[i,:]

def get_column(board, j):
	return board[:,j]

def get_block(board, i, j):
	n = int(np.sqrt(board.shape[0]))
	sub_i = int(i/n)
	sub_j = int(j/n)
	return board[n*sub_i:n*sub_i+n, n*sub_j:n*sub_j+n]

def get_possible_values(board, i, j):
	values = set()
	values.update(get_row(board, i))
	values.update(get_column(board, j))
	values.update(get_block(board, i, j).flatten())
	values.discard(0)
	return set(range(1,10)).difference(values)

def get_possible_indices(board, i, j, n):
	possible_indices = []

	if i + n < 9:
		if board[i+n][j] == 0:
			if n in get_possible_values(board, i+n, j):
				possible_indices.append((i+n, j))

	if i - n >= 0:
		if board[i-n][j] == 0:
			if n in get_possible_values(board, i-n, j):
				possible_indices.append((i-n, j))

	if j + n < 9:
		if board[i][j+n] == 0:
			if n in get_possible_values(board, i, j+n):
				possible_indices.append((i, j+n))

	if j - n >= 0:
		if board[i][j-n] == 0:
			if n in get_possible_values(board, i, j-n):
				possible_indices.append((i, j-n))
	
	return possible_indices

def set_missing_values(board):

	while len(board[board == 0]) > 0:

		changed = False

		for i in range(9):
			for j in range(9):
				if board[i][j] == 0:
					vals = get_possible_values(board, i, j)
					
					if len(vals) == 1:
						board[i][j] = list(vals)[0]
						changed = True

		if changed == False:
			return

def set_constraint_values(board, constraint_board):

	while len(board[constraint_board != 0]) > 0:

		changed = False

		for i in range(9):
			for j in range(9):
				if constraint_board[i][j] != 0 & board[i][j] == 0:
					n = constraint_board[i][j]
					idxs = get_possible_indices(board, i, j, n)

					if len(idxs) == 1:
						board[idxs[0]] = n
						constraint_board[i][j] = 0
						changed = True

		if changed == False:
			return

def set_all(board, constraint_board):
	print("solving...")
	
	while True:
		n_nonzero_old = len(board[board == 0])
		set_constraint_values(board, constraint_board)
		set_missing_values(board)
		n_nonzero_new = len(board[board == 0])

		if n_nonzero_new == 0:
			print("solved")
			return

		if n_nonzero_old == n_nonzero_new:
			print("no more changes")
			break

		n_nonzero_old = n_nonzero_new

	return


################################################################
################################################################
################################################################


board = np.array([[0]*9]*9)

constraint_board = np.array([
	[2,0,0,0,7,1,8,3,6],
	[0,0,0,0,0,0,0,2,0],
	[0,0,5,0,0,5,4,0,2],
	[0,0,0,1,0,0,5,0,1],
	[8,3,3,0,1,0,2,4,4],
	[3,0,4,0,0,3,0,0,0],
	[6,0,2,3,0,0,5,0,0],
	[0,4,0,0,0,0,0,0,0],
	[7,2,7,3,1,0,0,0,3]
])

print("\nboard:\n", board, '\n')
print("constraint board:\n", constraint_board, '\n')

set_all(board, constraint_board)

print("\nsolved board:\n", board, '\n')



