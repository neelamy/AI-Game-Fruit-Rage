import time
import string
from collections import defaultdict
from copy import deepcopy 
import math

class FruitRage:

	# initilaize variables
	def __init__(self, board_size, fruit_type, time_remaining, board):
		self.board_size = board_size
		self.fruit_type = fruit_type
		self.time_remaining = time_remaining
		self.board = board
		self.max_depth = 2
		self.start_time = time.time()
		self.cutoff_time = time.time()


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


	# perform dfs to find all connected fruits
	def findConnectedComponent(self,i,j, visited, fruit_type):

		# array to get neighbours of a cell
		rowno = [ -1,  0, 0, 1];
   	 	colno = [ 0, -1, 1,  0];
		
		# Mark this cell as visited
		visited[i][j] = True
		count = 1
		# Recur for all connected neighbours
		for k in range(4):
			if self.isSafe(i + rowno[k], j + colno[k], visited,fruit_type, self.board ):
				count += self.findConnectedComponent(i + rowno[k], j + colno[k], visited, fruit_type)
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
		if depth >= self.max_depth or time.time() - self.start_time >= self.cutoff_time:
			return True
		

	# check if terminal state has been achieved
	def is_terminal(self, local_board):
		flag =  False
		for row in xrange(self.board_size):
			for col in xrange(self.board_size):
				if local_board[row][col] == '*': continue
				flag = True
				break
		return False if flag else True



	# This function returns the max score possible
	def max_value(self, alpha, beta, local_board, depth, score):

		# check for cutoff state
		if self.isCutoffstate(depth) or self.is_terminal(local_board) :
			#score = self.evaluate_score()
			return score

		# initialize variables
		v = float("-Inf")
		visited_max = [[ False for _ in xrange(self.board_size)] for _ in xrange(self.board_size)]

		# check all cells for possible move
		for row in xrange(self.board_size):
			for col in xrange(self.board_size):

				# skip if cell has been visited or if its '*''
				if visited_max[row][col] == True or local_board[row][col]== '*': continue
		
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
		if self.isCutoffstate(depth) or self.is_terminal(local_board) :
			return score

		# initialize variables
		visited_min = [[ False for _ in xrange(self.board_size)] for _ in xrange(self.board_size)]
		v = float("Inf")

		# check all cells for possible move
		for row in xrange(self.board_size):
			for col in xrange(self.board_size):

				# skip if cell has been visited or if its '*''
				if visited_min[row][col] == True or local_board[row][col]== '*': continue
				
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
	def getBestMove(self):

		# initialize variables
		visited = [[ False for j in xrange(self.board_size)] for i in xrange(self.board_size)]
		best_move_count = -float("Inf")
		best_move_cell = []
		alpha = float("-Inf")
		beta = float("Inf") 
		final_board = self.board
		v = float("-Inf")

		# traverse all cells for possible best move
		for row in range(self.board_size):
			for col in range(self.board_size):

				# skip if cell has been visited or if its '*''
				if visited[row][col] == True or self.board[row][col]== '*': continue

				# apply gravity on selected cell and call min function
				new_board, max_count = self.apply_gravity([row, col], visited, self.board)

				#current_move_count = self.min_value(alpha, beta, new_board, 1, max_count)
				v = max( v, self.min_value(alpha, beta, new_board, 1, max_count * max_count))

				# save best move in best_move_count
				if v > best_move_count:
					best_move_count = v
					best_move_cell = [row,col]
					final_board = new_board
				if v >= beta : return v

				#update alpha
				alpha = max(v, alpha)
				#print best_move_count

				if self.max_depth == 0 : return final_board, best_move_cell

		return final_board, best_move_cell


	def getConnectedElements(self):
		visited = [[ False for _ in xrange(self.board_size)] for _ in xrange(self.board_size)]
		count = 0
		total_fruits = 0
		# traverse all cells for possible best move
		for row in range(self.board_size):
			for col in range(self.board_size):
				if visited[row][col] == True or self.board[row][col]== '*': continue
				total_fruits += self.findConnectedComponent(row,col, visited, self.board[row][col])
				count += 1
		
		return count, total_fruits

	
	def setCutoffTime(self, n):
		self.cutoff_time = self.time_remaining / math.log(1 + n )


	def setdepth(self, n):
		# open calibrate file
		input_file = "calibration.txt"
		with open(input_file,'r') as cal_inp: 
			# get all the contents of the file in variable content
			contents = [x.strip('\n') for x in cal_inp.readlines()]
			cal_time, cal_node = contents[0].split()
		nodes_that_can_be_covered = (float(cal_node) /float(cal_time)) * self.cutoff_time
		branching_factor = n if n > 2 else 2
		self.max_depth = int(math.log(((nodes_that_can_be_covered * (branching_factor - 1)) + 1),branching_factor) - 1)


	# get the best move for given input
	def startgame(self):
		connected_comp, total_fruits = self.getConnectedElements()
		self.setCutoffTime(total_fruits)
		self.setdepth(connected_comp)
		self.start_time = time.time()
		final_board, max_count_cell =  self.getBestMove()

		#change cell no to required format and return
		cell_loc = self.get_cell_location(max_count_cell)
		#print cell_loc
		return cell_loc, final_board 



# this will parse the given input file
def parse_input():

	# open input file
	input_file = "input.txt"
	with open(input_file,'r') as inp: 

		# get all the contents of the file in variable content
		contents = [x.strip('\n') for x in inp.readlines()]
		board_size = int(contents[0])

		# get no of rows 
		fruit_type = int(contents[1])

		# get number of lizards
		time_remaining = float(contents[2])

		# remaining content is matrix for board
		board = []
		for line in contents[3 :]:
			row = [ int(x) if x.isdigit() else x for x in list(line)]
			board.append(row)

	# return all values to main function
	return board_size, fruit_type, time_remaining, board



# write the output in output file
def write_ouput(loc, board):

	# open output file
	out_file =  "output.txt"
	with open(out_file, 'w') as out: 

		# write pass or fail status
		out.write(loc + "\n")
		
		# if new nursery matrix is present then add that to output file
		if board:
			for line in board:
				line = [ str(x) if x!='*' else x for x in list(line)]
				l = "".join(line)
				out.write(l + "\n")


# main function
def main():

		# parse input file to get the input variables
		board_size, fruit_type, time_remaining, board = parse_input()
		#print board
		cell_loc, board = FruitRage(board_size, fruit_type, time_remaining, board).startgame()

		# write the output in output file
		write_ouput(cell_loc, board)


if __name__ == '__main__':
 
	main()
