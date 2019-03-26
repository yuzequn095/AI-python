from __future__ import absolute_import, division, print_function
import copy
import random
# import numpy as np 
# python install path mess up, can't use numpy

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}


# Create a Node class to store relevant information 
class Node:
    def __init__(self, matrix, score, player, move):
        # Set relevant information for this node
        self.matrix = matrix
        self.score = score
        # Set max player as 0 and chance player as 1
        self.player = player
        # Set the last move
        self.move = move
        # Connect with node's parent and children
        self.parent = []
        self.children = []


class Gametree:
    """main class for the AI"""

    # Hint: Two operations are important. Grow a game tree, and then compute minimax score.
    # Hint: To grow a tree, you need to simulate the game one step.
    # Hint: Think about the difference between your move and the computer's move.
    def __init__(self, root_state, depth_of_tree, current_score):
        # Initialize depth, and score
        self.height = depth_of_tree
        self.score = current_score
        self.root_state = root_state
        # Set root node
        self.root = Node(root_state, current_score, "max", -1)
        # To record terminal node
        self.terminal = []

    # Explicitly construct a game tree from any state of the game
    # Hints from DI slide: When creating children node, make a deep copy
    #                      Make sure to expand all nodes
    def grow_tree(self, root, height):
        # Check the depth of tree (3)
        if height == 0:
            # print("Height = 0, search ends")
            # growing completed this turn
            self.terminal.append(root)
            # print("Appended to terminal")

        else:
            # print("Height > 0, search continue")
            # grow all children node in next depth
            # player - computer - player
            # if this is max player turn: perform moves (root node)
            if root.player == "max":
                # print("max player")
                # for 4 directions
                for d in range(4):
                    # print("explore each direction")
                    # make deep copy
                    parent_simulator = Simulator(copy.deepcopy(root.matrix), root.score)
                    # perform desire action (move)
                    # for d in range(4):
                    # move in each direction
                    if (parent_simulator.move(d)):
                        # print("if can move")
                        # grow tree with a new child node
                        child_node = Node(copy.deepcopy(parent_simulator.tileMatrix), parent_simulator.total_points, "chance", d)
                        # check child is distinct from parent
                        # a = np.array(root)
                        # b = np.array(child_node)
                        # c = a - b
                        # yes for distinct
                        # if sum(c) != 0:
                        if root.matrix != child_node.matrix:
                            # print("if different")
                            # connect into tree
                            root.children.append(child_node)
                            child_node.parent.append(root)
                # check if no child node can be expanded
                if len(root.children) == 0:
                    # print("if no child")
                    # insert to terminal
                    self.terminal.append(root)

            # else if this is chance player turn: set a tile
            elif root.player == "chance":
                # print("chance player")
                # make a deep copy
                parent_simulator = Simulator(copy.deepcopy(root.matrix), root.score)
                # set a random 2-tile
                # parent_simulator.placeRandomTile()
                # set each possible 2-tile
                # onlu 4 * 4 matrix
                for r in range(4):
                    for c in range(4):
                        # check if empty
                        if root.matrix[r][c] == 0:
                            # print("find empty tile")
                            # grow tree with a new child node
                            child_node = Node(copy.deepcopy(parent_simulator.tileMatrix), parent_simulator.total_points, "max", -1)
                            child_node.matrix[r][c] = 2
                            # check child node is distinct
                            # a = np.array(root_state)
                            # b = np.array(child_node)
                            # c = a - b
                            # if sum(c) != 0:
                                # print("if different")
                            # connect into tree
                            root.children.append(child_node)
                            child_node.parent.append(root)
            # check if no child node can be expanded
            if len(root.children) == 0:
                # print("if no child")
                # insert to terminal
                self.terminal.append(root)

        # recursively call grow_tree and update parameters
    # for n in root_state.children:
    # self.grow_tree(n, height_of_tree - 1)


    # tree generator drive
    def tree_template(self, root, height):
        # call function to generate tree
        # grow root first
        # print("grow tree root")
        self.grow_tree(root, height)

        # grow from child
        for c in root.children:
            # print("grow tree child")
            # call function to generate from child
            self.tree_template(c, height - 1)


    # expectimax for computing best move
    def expectimax(self, state):
        # print("expectmax")
        # check terminal
        if state in self.terminal:
            # print("if terminal")
            # calculate payoff
            return self.payoff(state)
        # max player case
        elif state.player == "max":
            # print("max")
            value = -999
            for c in state.children:
                value = max(value, self.expectimax(c))
            return value
    
        # chance player case
        elif state.player == "chance":
            # print("chance")
            value = 0
            for c in state.children:
                value = value + self.expectimax(c) * self.chance(state)
            return value


    # calculate pay off
    def payoff(self, node):
        # print("payoff")
        # get node score
        return node.score


    # probability of child node be visisted
    def chance(self, node):
        # print("chance")
        # check the number of children
        # each child has same probability
        num_child = len(node.children)
        return 1.0 / num_child


    # function to return best decision to game
    def compute_decision(self):
        # print("computer decision")
        # grow the tree
        # self.grow_tree(self.root, 3 - self.depth_of_tree)
        # print("call tree template")
        self.tree_template(self.root, self.height)
        # set value and move
        max_value = 0
        optimal_move = 0

        # make decision from root
        for c in self.root.children:
            # print("check children")
            # get result from expectmax
            # print("get cur_value")
            cur_value = self.expectimax(c)
            # check if value is valid
            if cur_value > max_value:
                # print("update value")
                max_value = cur_value
                # mark move
                optimal_move = c.move
        # return move index
        # change this return value when you have implemented the function
        return optimal_move


# mostly copy&paste from 2048.py
# make slightly changes for using 
class Simulator:
    # Need methods that will take in a move and board state
    #  and manipulate the current board state
    # init class for simulator
    def __init__(self, matrix, score):
        self.total_points = score
        self.default_tile = 2
        self.board_size = 4
        # pygame.init()
        # self.surface = pygame.display.set_mode((400, 500), 0, 32)
        # self.tileMatrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.undoMat = []
        self.tileMatrix = matrix

    # --- May can be used to move tile ---
    def move(self, direction):
        self.addToUndo()
        for i in range(0, direction):
            self.rotateMatrixClockwise()
        if self.canMove():
            self.moveTiles()
            self.mergeTiles()
            return True
        # self.placeRandomTile()
        else:
            return False
        for j in range(0, (4 - direction) % 4):
            self.rotateMatrixClockwise()

    # self.printMatrix()

    # If need random place for chance
    def placeRandomTile(self):
        while True:
            i = random.randint(0, self.board_size - 1)
            j = random.randint(0, self.board_size - 1)
            if self.tileMatrix[i][j] == 0:
                break
        self.tileMatrix[i][j] = 2

    # for move
    def moveTiles(self):
        tm = self.tileMatrix
        for i in range(0, self.board_size):
            for j in range(0, self.board_size - 1):
                while tm[i][j] == 0 and sum(tm[i][j:]) > 0:
                    for k in range(j, self.board_size - 1):
                        tm[i][k] = tm[i][k + 1]
                    tm[i][self.board_size - 1] = 0

    # for move
    def mergeTiles(self):
        tm = self.tileMatrix
        for i in range(0, self.board_size):
            for k in range(0, self.board_size - 1):
                if tm[i][k] == tm[i][k + 1] and tm[i][k] != 0:
                    tm[i][k] = tm[i][k] * 2
                    tm[i][k + 1] = 0
                    self.total_points += tm[i][k]
                    self.moveTiles()

    # --- May can be used if game over ---
    def checkIfCanGo(self):
        tm = self.tileMatrix
        for i in range(0, self.board_size ** 2):
            if tm[int(i / self.board_size)][i % self.board_size] == 0:
                return True
        for i in range(0, self.board_size):
            for j in range(0, self.board_size - 1):
                if tm[i][j] == tm[i][j + 1]:
                    return True
                elif tm[j][i] == tm[j + 1][i]:
                    return True
        return False

    # --- May can be used if movable ---
    def canMove(self):
        tm = self.tileMatrix
        for i in range(0, self.board_size):
            for j in range(1, self.board_size):
                if tm[i][j - 1] == 0 and tm[i][j] > 0:
                    return True
                elif (tm[i][j - 1] == tm[i][j]) and tm[i][j - 1] != 0:
                    return True
        return False

    # manipulate matrix functions
    def rotateMatrixClockwise(self):
        tm = self.tileMatrix
        for i in range(0, int(self.board_size / 2)):
            for k in range(i, self.board_size - i - 1):
                temp1 = tm[i][k]
                temp2 = tm[self.board_size - 1 - k][i]
                temp3 = tm[self.board_size - 1 - i][self.board_size - 1 - k]
                temp4 = tm[k][self.board_size - 1 - i]
                tm[self.board_size - 1 - k][i] = temp1
                tm[self.board_size - 1 - i][self.board_size - 1 - k] = temp2
                tm[k][self.board_size - 1 - i] = temp3
                tm[i][k] = temp4

    def isArrow(self, k):
        return (k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT)

    def getRotations(self, k):
        if k == pygame.K_UP:
            return 0
        elif k == pygame.K_DOWN:
            return 2
        elif k == pygame.K_LEFT:
            return 1
        elif k == pygame.K_RIGHT:
            return 3

    def convertToLinearMatrix(self):
        m = []
        for i in range(0, self.board_size ** 2):
            m.append(self.tileMatrix[int(i / self.board_size)][i % self.board_size])
        m.append(self.total_points)
        return m

    # For undo
    def addToUndo(self):
        self.undoMat.append(self.convertToLinearMatrix())

    def undo(self):
        if len(self.undoMat) > 0:
            m = self.undoMat.pop()
            for i in range(0, self.board_size ** 2):
                self.tileMatrix[int(i / self.board_size)][i % self.board_size] = m[i]
            self.total_points = m[self.board_size ** 2]
            self.printMatrix()
