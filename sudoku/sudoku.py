from __future__ import print_function
import random, copy

class Grid:
	# problem is array given
	def __init__(self, problem):
		self.spots = [(i, j) for i in range(1,10) for j in range(1,10)]
		self.domains = {}
		# Need a dictionary that maps each spot to its related spots
		self.peers = {}
		# set peers
		self.set_peers()
		self.parse(problem)

	def parse(self, problem):
		for i in range(0, 9):
			for j in range(0, 9):
				c = problem[i*9+j]
				# test: print("c is:", c)
				# if c is empty ('.') then domain is 1-9
				if c == '.':
					self.domains[(i+1, j+1)] = range(1,10)
					# test: print("now domains: ", self.domains[(i+1,j+1)])
				# else the domain is fixed (self)
				else:
					self.domains[(i+1, j+1)] = [ord(c)-48]
					# test: print("now domains: ", self.domains[(i + 1, j + 1)])

	def display(self):
		for i in range(0, 9):
			for j in range(0, 9):
				d = self.domains[(i+1,j+1)]
				# test: print("d is: ", d)
				# if domain is length 1, then the spot is the domain self
				if len(d) == 1:
					print(d[0], end='')
				#if (i+1, j+1) in self.sigma:
					#print(self.sigma[(i+1, j+1)], end='')
				# else the spot is '.'
				else:
					print('.', end='')
				# each col
				if j == 2 or j == 5:
					print(" | ", end='')
			print()
			# each row
			if i == 2 or i == 5:
				print("---------------")

	# function to set peers for a specify spot
	def set_peers(self):
		# use self.peers to save
		# use loop to go over each spot
		for i in range(1, 10):
			for j in range(1, 10):
				#print("Now set for: (", i, ", ", j, ")" )
				tmp_peers = []
				# first collect the row for each spot
				for row in range(1, 10):
					# update index for row
					# skip the current one
					if row == i:
						continue
					else:
						# map (i,j) to all peers in row
						tmp_peers.append((row, j))
				# second collect the col for each spot
				for col in range(1, 10):
					# skip the current one
					if col == j:
						continue
					else:
						# map (i, j) to all peers in col
						tmp_peers.append((i, col))
				# last collect the 3*3 grid for each spot
				# set row bounds
				# 1 - 3
				if (i == 1) or (i == 2) or (i == 3):
					low_row = 1
					high_row = 4
				# 4 - 6
				elif (i == 4) or (i == 5) or (i == 6):
					low_row = 4
					high_row = 7
				# 7 - 9
				else:
					low_row = 7
					high_row = 10
				# set col bounds
				# 1 - 3
				if (j == 1) or (j == 2) or (j == 3):
					low_col = 1
					high_col = 4
				# 4 - 6
				elif (j == 4) or (j == 5) or (j == 6):
					low_col = 4
					high_col = 7
				# 7 - 9
				else:
					low_col = 7
					high_col = 10
				for row in range(low_row, high_row):
					for col in range(low_col, high_col):
						# skip the current one
						if (row, col) == (i, j):
							continue
						else:
							# map(i, j) to all peers in grid
							tmp_peers.append((row, col))
				# set peers
				self.peers[(i, j)] = tmp_peers
		# test peers
		#for i in range(1, 10):
			#for j in range(1, 10):
				#print("For (", i, ", ", j, "):")
				#for p in self.peers[(i,j)]:
					#print("p is: ", p)

class Solver:
	def __init__(self, grid):
		# sigma is the assignment function
		# sigma is a dict of spot:value pairs
		self.sigma = {}
		self.grid = grid
		# set sigma
		self.set_sigma()
		# set unassignment array
		#self.un_assign = []

	# function to display solution
	def true_display(self):
		for i in range(0, 9):
			for j in range(0, 9):
				x = i + 1
				y = j + 1
				#d = self.domains[(i+1,j+1)]
				# test: print("d is: ", d)
				# if domain is length 1, then the spot is the domain self
				if (x, y) in self.sigma:
					print(self.sigma[(x, y)], end='')
				# else the spot is '.'
				else:
					print('.', end='')
				# each col
				if j == 2 or j == 5:
					print(" | ", end='')
			print()
			# each row
			if i == 2 or i == 5:
				print("---------------")

	# function to set sigma
	def set_sigma(self):
		# for each (i, j) in grid
		for i in range(1, 10):
			for j in range(1, 10):
				# set spot
				spot = (i, j)
				# check if spot is assigned
				if len(self.grid.domains[spot]) == 1:
					# if it is, then assign spot:value to sigma
					self.sigma[spot] = self.grid.domains[spot][0]
				# set default value
				else:
					self.sigma[spot] = 0
		# test sigma
		#for i in range(1, 10):
			#for j in range(1, 10):
				#spot = (i, j)
				#print("Sigma for (",i, ",", j, ") is: ", self.sigma[spot] )

	# function to decide if problem be solved
	def solve(self):
		# default: return True
		# return the result from main part of this program
		#print("Call search")
		return self.back_search(self.sigma, self.grid.domains)

	# main function to play sudoku
	#def back_search(self, sigma, unassign, domains):
	def back_search(self, sigma, domains):
		#print("search start")
		#print("Check finish")
		# check if finish: 0->True, 1->False
		finish = 0
		un_assign = []
		# go over sigma
		for s in sigma:
			# check un_assignment exists
			if sigma[s] == 0:
				finish = 1
				# add to un_assign
				un_assign.append(s)
		# no un_assignment exists
		if finish == 0:
			return True
		# set list for infer
		infer_list = {}
		# make decision set value
		#print("Loop in un_assign")
		# take the spot with the smallest domain value from un_assign array
		l, sp = min((len(domains[u]), u) for u in un_assign)
		#print("Pick spot: (", sp[0], ",", sp[1], ")")
		#print("Check ")
		# for each possible value in domains
		#print("Check value in domains")
		for v in domains[sp]:
				# check if value consistence
				# print("Check value as: ", v)
				if_cons = self.consistent(sp, v, sigma)
				if if_cons:
					# print("Consistent passed")
					# add this value to sigma
					# new branch in my tree
					sigma[sp] = v
					# print("New sigma[(",sp[0],",",sp[1],")]: ", v)
					# set inference
					tmp_sigma = copy.deepcopy(sigma)
					tmp_domain = copy.deepcopy(domains)
					# get update infer_list and if_inf
					infer_list, if_inf = self.infer(tmp_sigma, sp, tmp_domain)
					# if not failure
					if if_inf:
						#print("Infer passed")
						# add inferences to sigma
						for ip in infer_list:
							#print("update sigma")
							sigma[ip] = infer_list[ip]
							# update unassign
							#unassign.remove(ip)
						# call function recursively
						#print("call search again")
						if_bs = self.back_search(self.sigma, self.grid.domains)
						# check if_bs
						if if_bs:
							#print("recursive passed")
							# return
							return True
				# remove {var:value}(not even assigned) and inferences from sigma
				else:
					# print("Consistent not passed")
					sigma[sp] = 0
					for i in infer_list:
						sigma[i] = 0
		# default return
		return False


	# function to check if value is consistent with spot
	def consistent(self, spot, value, sigma):
		# print("Now in consistent")
		# check if conflict with values in peer
		for p in self.grid.peers[spot]:
			# check if p has been assigned in sigma
			# check if value has been used
			if value == sigma[p]:
				return False
			# not assign, next peer
			else:
				continue
		# no conflict
		return True

	def infer(self, sigma, spot, domains):
		# print("Now in infer")
		# get index
		#x = spot[0]
		#y = spot[1]
		# set value can be used
		#tmp_domain = {}
		# set empty peer
		empty_peer = []
		# set infer list
		infer_list = {}
		# infer for all possible peers of spot
		for p in self.grid.peers[spot]:
			# check if assigned already
			if sigma[p] == 0:
				# update domain and peer
				domains[p] = list(range(1, 10))
				empty_peer.append(p)
		# update domain
		for p in empty_peer:
			# if value used
			if sigma[spot] in domains[p]:
				domains[p].remove(sigma[spot])
		# check all empty peers
		for p in empty_peer:
			# if no value can be used to set new value
			if len(domains[p]) == 0:
				return {}, False
			# else set
			if len(domains[p]) == 1:
				tmp_value = domains[p][0]
				# print("tmp value: ", tmp_value)
				con_if = consistent(p, tmp_value, sigma)
				# if consistent
				if con_if:
					# print("Consist passed")
					# set value
					sigma[p] = tmp_value
					infer_list[p] = tmp_value
					# recursive
					new_infer, infer_if = self.infer(sigma, p, domains)
					# check if_infer
					if infer_if:
						# assign infer
						for i in new_infer:
							# update infer_list from recursive
							infer_list[i] = new_infer[i]
					else:
						sigma[p] = 0
						return {}, False
					break
				else:
					return {}, False
		# default return
		return infer_list, True



easy = ["..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..",
"2...8.3...6..7..84.3.5..2.9...1.54.8.........4.27.6...3.1..7.4.72..4..6...4.1...3"]

hard = ["4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......",
"52...6.........7.13...........4..8..6......5...........418.........3..2...87....."]

print("====Problem====")
#g = Grid(easy[0])
g1 = Grid(hard[0])
#Display the original problem
#g.display()
g1.display()
#s = Solver(g)
s1 = Solver(g1)
#if s.solve():
	#print("====Solution===")
	#Display the solution
	#Feel free to call other functions to display
	#s.true_display()
if s1.solve():
	print("====Solution===")
	# Display the solution
	# Feel free to call other functions to display
	s1.true_display()
else:
	print("==No solution==")

