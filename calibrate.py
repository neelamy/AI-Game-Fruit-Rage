import time
import string
import math
from collections import defaultdict
from copy import deepcopy 

class FruitRage:

	# initilaize variables
	def __init__(self):

		'''
		Input :
		10
		4
		300
		0123012301
		1032103210
		0123012301
		1032103210
		0123012301
		1032103210
		0123012301
		1032103210
		0123012301
		1032103210'''

		self.board_size = 10
		self.fruit_type = 4
		self.time_remaining = 300
		self.board = [[0, 1, 2, 3, 0, 1, 2, 3, 0, 1],
					 [1, 0, 3, 2, 1, 0, 3, 2, 1, 0], 
					 [0, 1, 2, 3, 0, 1, 2, 3, 0, 1],
					 [1, 0, 3, 2, 1, 0, 3, 2, 1, 0],
					 [0, 1, 2, 3, 0, 1, 2, 3, 0, 1], 
					 [1, 0, 3, 2, 1, 0, 3, 2, 1, 0], 
					 [0, 1, 2, 3, 0, 1, 2, 3, 0, 1], 
					 [1, 0, 3, 2, 1, 0, 3, 2, 1, 0], 
					 [0, 1, 2, 3, 0, 1, 2, 3, 0, 1], 
					 [1, 0, 3, 2, 1, 0, 3, 2, 1, 0]]

		self.start_time = time.time()
		self.node = 0


	# A function to check if a given cell (row, col) can be included in dfs
	def isSafe(self, i, j, visited, fruit_type, board_copy):
		# row number is in range, column number is in range and fruit type is same 
    	# and cell has not yet visited
		return (i >= 0 and i < self.board_size and 
				j >= 0 and j < self.board_size and 
				not visited[i][j] and board_copy[i][j] == fruit_type)
	

	# perform dfs to find all connected fruits
	def dfs(self,i,j, visited, fruit_type, board_copy,selected_path = {}):

		# array to get neighbours of a cell
		rowno = [ -1,  0, 0, 1];
   	 	colno = [ 0, -1, 1,  0];
		
		# Mark this cell as visited
		visited[i][j] = True
		count = 1 
		selected_path[j] = max(selected_path[j], i) if selected_path[j] else i
		board_copy[i][j] = '*'

		# Recur for all connected neighbours
		for k in range(4):
			if self.isSafe(i + rowno[k], j + colno[k], visited,fruit_type, board_copy ):
				count += self.dfs(i + rowno[k], j + colno[k], visited, fruit_type, board_copy, selected_path)
		return count


	# return cell location in required format
	def get_cell_location(self, max_count_cell):
		if max_count_cell ==[] : return ""
		column_letter = dict(zip( range(len(string.uppercase)) , string.uppercase))
		return column_letter[max_count_cell[1]] + str(max_count_cell[0] + 1) 


	# update board by removing fruit from given path
	def update_board(self, selected_path, board_copy):

		# pick all columns one by one that needs to be updated
		for col in selected_path:

			# row is set to row from where board will be updated
			row = selected_path[col]
			row_to_be_copied = row - 1
			while row_to_be_copied > -1 :

				# skip row in case it contain * else drop the element down 
				if board_copy[row_to_be_copied][col] == '*' : row_to_be_copied -=1
				else:
					board_copy[row][col] = board_copy[row_to_be_copied][col]
					board_copy[row_to_be_copied][col] = '*'
					row -= 1
					row_to_be_copied -= 1



	# apply gravity and bring fruits down in empty cell
	def apply_gravity(self, loc, visited, local_board):
		board_copy = deepcopy(local_board)

		# initialize variables
		row, col = loc
		fruit_type = local_board[row][col]
		selected_path = defaultdict(list)

		# call dfs to get all fruits that will be collected		
		count = self.dfs(row, col, visited, fruit_type, board_copy, selected_path)
		
		# update the board
		self.update_board(selected_path,board_copy)
		return board_copy, count



	# check if cutoff condition is true
	def isCutoffstate(self, depth):
		if depth >= self.max_depth or time.time()- self.start_time > 275 :return True


	# This function returns the max score possible
	def max_value(self, alpha, beta, local_board, depth, score):

		# check for cutoff state
		if self.isCutoffstate(depth): return score

		# initialize variables
		v = float("-Inf")
		visited_max = [[ False for _ in xrange(self.board_size)] for _ in xrange(self.board_size)]

		# check all cells for possible move
		for row in xrange(self.board_size):
			for col in xrange(self.board_size):

				# skip if cell has been visited or if its '*''
				if visited_max[row][col] == True or local_board[row][col]== '*': continue
				self.node += 1
				
				# update board for selected move
				new_board, max_count = self.apply_gravity([row, col], visited_max, local_board)
				max_count *= max_count
				v = max(v, self.min_value(alpha, beta, new_board, depth + 1, score + max_count))

				# check for pruning - alpha cut
				if v >= beta : return v

				#update alpha
				alpha = max(v, alpha)
		return v 



	# This function returns the min score possible
	def min_value(self, alpha, beta, local_board, depth, score):

		# check for cutoff state
		if self.isCutoffstate(depth) : return score

		# initialize variables
		visited_min = [[ False for _ in xrange(self.board_size)] for _ in xrange(self.board_size)]
		v = float("Inf")

		# check all cells for possible move
		for row in xrange(self.board_size):
			for col in xrange(self.board_size):

				# skip if cell has been visited or if its '*''
				if visited_min[row][col] == True or local_board[row][col]== '*': continue
				self.node += 1

				# update board for selected move
				new_board, min_count = self.apply_gravity([row, col], visited_min, local_board)
				min_count *= min_count
				v = min(v, self.max_value(alpha, beta, new_board, depth + 1, score - min_count))

				# check for pruning - beta cut
				if v <= alpha : return v

				#update beta
				beta = min(v, beta)
		return v 


	# select all possible move and return the one with max score
	def Calibrate(self):

		out_file =  "calibration.txt"
		with open(out_file, 'w') as cal_out:

			# initialize variables
			for d in xrange(4, 5):
				self.start_time = time.time()
				self.max_depth = d
				self.node = 0
				visited = [[False for _ in xrange(self.board_size)] for _ in xrange(self.board_size)]
				alpha = float("-Inf")
				beta = float("Inf")
				v = float("-Inf")

			# traverse all cells for possible best move
				for row in range(self.board_size):
					for col in range(self.board_size):

						# skip if cell has been visited or if its '*''
						if visited[row][col] == True or self.board[row][col]== '*': continue
						self.node += 1

						# apply gravity on selected cell and call min function
						new_board, max_count = self.apply_gravity([row, col], visited, self.board)

						#current_move_count = self.min_value(alpha, beta, new_board, 1, max_count)
						v = max( v, self.min_value(alpha, beta, new_board, 1, max_count * max_count))

						# save best move in best_move_count
						if v >= beta : return v

						#update alpha
						alpha = max(v, alpha)
			
				cal_out.write(str(time.time() - self.start_time) + " " + str(self.node) +"\n")


# main function
def main():

		FruitRage().Calibrate()		


if __name__ == '__main__':
 
	main()
