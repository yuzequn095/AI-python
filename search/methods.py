from __future__ import print_function
#Use priority queues from Python libraries, don't waste time implementing your own
from heapq import *
#Queue using list and deque
from collections import deque
#Math functions for a*
import math

ACTIONS = [(0,-1),(-1,0),(0,1),(1,0)]

class Agent:
    def __init__(self, grid, start, goal, type):
        self.grid = grid
        self.previous = {}
        self.explored = []
        self.start = start 
        self.grid.nodes[start].start = True
        self.goal = goal
        self.grid.nodes[goal].goal = True
        self.new_plan(type)
    def new_plan(self, type):
        self.finished = False
        self.failed = False
        self.type = type
        if self.type == "dfs" :
            self.frontier = [self.start]
            self.explored = []
        elif self.type == "bfs":
            self.frontier = deque([self.start])
            self.explored = []
        elif self.type == "ucs":
            self.frontier = [(0, self.start)]
            #heappush(self.frontier, (0, self.start))
            #set a dictionary to store path cost 
            self.path_cost = {self.start:0}
            #print("The cost for now node is: ", self.path_cost[self.start])
            self.explored = []
        elif self.type == "astar":
            print("A* start:")
            #almost same as 'ucs'
            #start_cost = self.euc_dis(self.start, self.goal)
            self.frontier = [(0, self.start)]
            #set a dictionary 
            self.path_cost = {self.start: 0}
            self.explored = []
    def show_result(self):
        current = self.goal
        while not current == self.start:
            current = self.previous[current]
            self.grid.nodes[current].in_path = True #This turns the color of the node to red
    def make_step(self):
        if self.type == "dfs":
            self.dfs_step()
        elif self.type == "bfs":
            self.bfs_step()
        elif self.type == "ucs":
            self.ucs_step()
        elif self.type == "astar":
            self.astar_step()
    def dfs_step(self):
        #check if start exists
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        current = self.frontier.pop()
        #print("current node: ", current)
        #Mark current node as checked and saved to explored. Set children with
        #around cells.
        self.grid.nodes[current].checked = True
        self.grid.nodes[current].frontier = False
        self.explored.append(current)
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        #Search grid using dfs for each node in children.
        for node in children:
            #See what happens if you disable this check here
            if node in self.explored or node in self.frontier:
                #print("explored before: ", node)
                continue
            #Check the node if this node is in our grid world.
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                #if this node can't reach
                if self.grid.nodes[node].puddle:
                    print("puddle at: ", node)
                else:
                    #set current node as previous node for the checking node
                    self.previous[node] = current
                    if node == self.goal:
                        self.finished = True
                        return
                    else:
                        #set this node to frontier as next start
                        self.frontier.append(node)
                        #set node as frontier
                        self.grid.nodes[node].frontier = True
            else:
                print("out of range: ", node)
    
    def bfs_step(self):
        #check if start exists
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        current = self.frontier.popleft()
        #print("current node: ", current)
        #Mark current node as checked and saved to explored. Set children for
        #current.
        self.grid.nodes[current].checked = True
        self.grid.nodes[current].frontier = False
        self.explored.append(current)
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        #Search grid using bfs for each node in children.
        for node in children:
            #See what happens if you disable this check here
            if node in self.explored or node in self.frontier:
                #print("explored before: ", node)
                continue
            #Check the node if this node is in our grid world.
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                #if this node can't reach
                if self.grid.nodes[node].puddle:
                    print("puddle at: ", node)
                else:
                    #set current node as previous node for the checking node
                    self.previous[node] = current
                    if node == self.goal:
                        self.finished = True
                        return
                    else:
                        #set current node to frontier as next start
                        self.frontier.append(node)
                        #set node as frontier
                        self.grid.nodes[node].frontier = True
            else:
                print("out of range: ", node)
    def ucs_step(self):
        #[Hint] you can get the cost of a node by node.cost()
        #check if start exits
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        #A loop expands one node from frontier
        #while self.frontier:
        #print("----------------------------------")
        #pop the node from self.frontier with lowest cost
        current = heappop(self.frontier)
        #set node as (a,b), set cost as int
        cur_node = current[1]
        cur_cost = current[0]
        #print("Now we get node: ", cur_node)
        #print("Now we get cost: ", cur_cost)
        #print("The path cost: ", self.path_cost[cur_node])
        #check current node reach goal
        #if cur_node == self.goal:
            #self.finished = True
            #return
        #remove from frontier and add to explored
        self.grid.nodes[cur_node].checked = True
        self.grid.nodes[cur_node].frontier = False
        self.explored.append(cur_node)
        #get children
        children = [(cur_node[0]+a[0], cur_node[1]+a[1]) for a in ACTIONS]
        #check each child 
        #print("Now check each child node")
        for node in children:
            #print("Now the child node: ", node)
            #check range
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                #if node not in explored
                if node not in self.explored:
                    #check puddle
                    if self.grid.nodes[node].puddle:
                        print("puddle at: ", node)
                    else:
                        #set current
                        self.previous[node] = cur_node
                        #check goal
                        if node == self.goal:
                            self.finished = True
                            print("Final cost: ", self.path_cost[cur_node] + self.grid.nodes[node].cost())
                            return
                        #if not in explored or frontier then add to frontier
                        if (self.path_cost[cur_node]+self.grid.nodes[node].cost(), node) not in self.frontier:
                            #print("not in explored or frontier")
                            self.path_cost[node] = self.path_cost[cur_node] + self.grid.nodes[node].cost()
                            heappush(self.frontier, (self.path_cost[node], node))
                            self.grid.nodes[node].frontier = True
                            #print("Child node inserted: ", node)
                        #exist but need to update
                        if (self.grid.nodes[node].cost() + self.path_cost[cur_node]) < self.path_cost[node]:
                            #print("need to update")
                            heappush(self.frontier,(self.grid.nodes[node].cost() + self.path_cost[cur_node], node))
                            self.path_cost[node] = self.grid.nodes[node].cost() + self.path_cost[cur_node]
                            #print("Child node updated: ", node)
                            self.grid.nodes[node].frontier = True
            else:
                print("out of range: ", node)
        #print("Now frontier: ", self.frontier)
        #if empty
        #self.failed = True
        #print("empty")
        #return

    #define a function to get heuristic cost for a*
    def euc_dis(self, node, goal):
        #get the square root of sum of square of difference
        return 10 * math.sqrt(math.pow(node[0] - goal[0], 2) + pow(node[1] - goal[1], 2))
    
   # def euc_dis(self, node, goal):
        #x = abs(node[0] - goal[0])
        #y = abs(node[1] - goal[1])
        #return 100 * (x + y)

    def astar_step(self):
        #[Hint] you need to declare a heuristic function for Astar
        #check if start exists
        #print("Now frontier: ", self.frontier)
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        #A loop expands one node from frontier
        #print("------------------")
        current = heappop(self.frontier)
        #set node as (a,b) and cost as int
        cur_node = current[1]
        cur_cost = current[0]
        #print("now pop: ", cur_node)
        #remove from frontier and add to explored
        self.grid.nodes[cur_node].checked = True
        self.grid.nodes[cur_node].frontier = False
        self.explored.append(cur_node)
        #get children
        children = [(cur_node[0]+a[0], cur_node[1]+a[1]) for a in ACTIONS]
        #check each child
        for node in children:
            print("Now child: ", node)
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                #if node not in explored
                if node not in self.explored:
                    #check puddle
                    if self.grid.nodes[node].puddle:
                        print("puddle at: ", node)
                    else:
                        #set previous
                        self.previous[node] = cur_node
                        #get real cost
                        real_cost = self.path_cost[cur_node] + self.grid.nodes[node].cost()
                        #self.path_cost[node] = real_cost
                        #print("real cost: ", real_cost)
                        #get h cost
                        h_cost = int(self.euc_dis(node, self.goal))
                        #print("h cost: ", h_cost)
                        
                        #print("Checking goal")
                        #check goal
                        if node == self.goal:
                            self.finished = True
                            print("Final cost: ", real_cost)
                            return
                        
                        #print("Frontier now: ", self.frontier)
                        #print("Checking in frontier")
                        #if not in explored or frontier then add to frontier
                        if((real_cost + h_cost), node) not in self.frontier:
                            #print("not in explored")
                            self.path_cost[node] = real_cost
                            #print("Now a* cost: ", real_cost + h_cost)
                            heappush(self.frontier, (real_cost + h_cost, node))
                            self.grid.nodes[node].frontier = True
                        #exist but need update
                        #print("path cost: ", self.path_cost[node])
                        #print("Checking update")
                        if(real_cost + h_cost < self.path_cost[node]):
                            #print("need to update")
                            heappush(self.frontier, (real_cost + h_cost, node))
                            self.path_cost[node] = real_cost
                            #print("update a* cost: ", real_cost + h_cost)
                            self.grid.nodes[node].frontier = True
                        #print("Frontier: ", self.frontier)
                else:
                    print("in explored already")
            else:
                print("out of range: ", node)
            

