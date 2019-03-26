from __future__ import absolute_import, division, print_function
from math import sqrt, log
import random


# Feel free to add extra classes and functions

class State:
    def __init__(self, grid, player):
        self.grid = grid
        self.piece = player
        # the visited times
        self.times = 0
        # the victory times
        self.points = 0
        # save parent and child
        self.child = []
        self.parent = []
        # set if state is terminal
        self.terminal = False
        # set if fully expand
        self.fullyexpand = False
        # set the move
        self.move = None
        # set possible move
        self.poss = []
        # set maxrc
        self.maxrc = len(grid) - 1
        # set game over
        self.over = False
        # set for help func
        self.grid_size = 52
        self.grid_count = 11
        self.winner = None

    # calculate the value of state
    def cal_best(self):
        return (self.points / self.times) + 2 * (sqrt((2 * log(self.parent.points)) / self.times))

    # what, where
    # fully defined with heuristics
    def checkExpand(self, grid):
        # call function to check possible move
        self.set_possible(grid)
        # check poss 
        if len(self.poss) == 0:
            return True

    def get_options(self, grid):
        # set occupied spots
        current_pcs = []
        for r in range(len(grid)):
            for c in range(len(grid)):
                if not grid[r][c] == '.':
                    current_pcs.append((r, c))
        # At the beginning of the game, curernt_pcs is empty
        if not current_pcs:
            return [(self.maxrc // 2, self.maxrc // 2)]
        # set optimal possible move
        min_r = max(0, min(current_pcs, key=lambda x: x[0])[0] - 1)
        max_r = min(self.maxrc, max(current_pcs, key=lambda x: x[0])[0] + 1)
        min_c = max(0, min(current_pcs, key=lambda x: x[1])[1] - 1)
        max_c = min(self.maxrc, max(current_pcs, key=lambda x: x[1])[1] + 1)
        # Options of reasonable next step moves
        options = []
        for i in range(min_r, max_r + 1):
            for j in range(min_c, max_c + 1):
                if not (i, j) in current_pcs:
                    options.append((i, j))
        # no spots can be used
        if len(options) == 0:
            self.winner = 'w'
            self.over = True
        return options

    # set possible spot to move
    def set_possible(self, grid):
        self.poss = self.get_options(grid)

    # make move from possible child
    def make_move(self):
        return random.choice(self.get_options(self.grid))

    # help functions
    def get_continuous_count(self, r, c, dr, dc):
        piece = self.grid[r][c]
        result = 0
        i = 1
        while True:
            new_r = r + dr * i
            new_c = c + dc * i
            if 0 <= new_r < self.grid_count and 0 <= new_c < self.grid_count:
                if self.grid[new_r][new_c] == piece:
                    result += 1
                else:
                    break
            else:
                break
            i += 1
        return result

    def check_win(self, r, c):
        n_count = self.get_continuous_count(r, c, -1, 0)
        s_count = self.get_continuous_count(r, c, 1, 0)
        e_count = self.get_continuous_count(r, c, 0, 1)
        w_count = self.get_continuous_count(r, c, 0, -1)
        se_count = self.get_continuous_count(r, c, 1, 1)
        nw_count = self.get_continuous_count(r, c, -1, -1)
        ne_count = self.get_continuous_count(r, c, -1, 1)
        sw_count = self.get_continuous_count(r, c, 1, -1)
        if (n_count + s_count + 1 >= 5) or (e_count + w_count + 1 >= 5) or (se_count + nw_count + 1 >= 5) or (
                ne_count + sw_count + 1 >= 5):
            self.winner = self.grid[r][c]
            self.over = True

    def set_piece(self, r, c):
        if self.grid[r][c] == '.':
            self.grid[r][c] = self.piece
            if self.piece == 'b':
                self.piece = 'w'
            else:
                self.piece = 'b'
            return True
        return False

    def rollout(self):
        simReward = {}
        while not self.over:
            r, c = self.make_move()
            self.set_piece(r, c)
            self.check_win(r, c)
        if self.winner == 'b':
            simReward['b'] = 0
            simReward['w'] = 1
        elif self.winner == 'w':
            simReward['b'] = 1
            simReward['w'] = 0
        return simReward


# pseudocode given
# heruistics( default policy; expansion )
# loop exits when reach "computation budget" ( number of iterations ) < 15s
# next move ( close to pieces ) - limit in small square
# rollout in Randplay
class MCTS:
    def __init__(self, grid, player):
        self.grid = grid
        self.piece = player
        # set leaf for mcts
        self.term = []
        # set root for mcts (deep copy for states)
        self.root = State(copy.deepcopy(self.grid), self.piece)

    def uct_search(self):
        # root state passed in
        # computational budget< 15sec ( large iteration )
        for i in range(0, 99):
            # use treePolicy select best child state or add child state to the
            #   root and select the added child state
            s = self.tree_policy(self.root)
            # use default policy runs simulation and returns an int for who won
            winner = self.default_policy(s)
            # back up update 
            self.back_up(s, winner)
        # end for
        # return action for board
        maxchild = self.best_child(self.root)
        return maxchild.move

    # def selection(self, state):
    # pass

    def tree_policy(self, state):
        # for terminal condition, check current player and won?
        s = state
        # if terminal 
        if s.terminal == True:
            return s
        # in not terminal
        while not s.terminal:
            # check if fully expanded
            # call function to set if fully expanded
            s.fullyexpand = s.checkExpand(s.grid)
            if s.fullyexpand == False:
                return expand(s)
            else:
                # set best child
                s = best_child(s)
            # end if
        # end while
        return s

    def expand(self, state):
        # get possible move from state
        # for m in state.poss:
        # if poss
        if len(state.poss) != 0:
            # pop from poss
            # move to get child
            child = state.poss.pop()
            # update child 
            state.child.append(child)
        return child

    def default_policy(self, state):
        # state return from tree( best child )
        # simulate until terminal
        # once terminal set result
        # check functions in Randplay
        # while not terminal
        # while not state.over:
        # pick random child and update s
        # state = state.make_move()
        state.rollout()
        # end while
        return state.winner

    def back_up(self, state, winner):
        # N(s) - how many times visit
        # Q(s) - win points
        while state:
            state.times += 1
            # check win, tie, lose
            if winner == state.player:
                state.points += 1
            elif winner == '.':
                state.points = state.points
            else:
                state.points -= 1
            state = state.parent
        # end while

    # def expansion(self, state):
    # pass
    def best_child(self, state):
        maxchild = None
        for c in state.child:
            if maxchild = None:
                maxchild = c
                continue
            if c.cal_best() > maxchild.cal_best():
                maxchild = c
        return maxchild

    # def simulation(self, state):
    # pass
    # def backpropagation(self, state, result):
    # pass
