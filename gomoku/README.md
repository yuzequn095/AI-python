Gomoku with Monte Carlo Tree Search
=========

The task is to implement the MCTS method for playing Gomoku. The base game engine is from [here](https://github.com/HackerSir/PygameTutorials/tree/master/Lesson04/Gomoku). 

The Game
-----
Gomoku is a popular game played on the Go board, following much simpler rules. 

- There are two players, one placing black pieces and the other white pieces, at the grid intersections of the board. 
- The two players take turns to place one piece each time. Pieces are never moved or removed from the board. 
- The players' goal is to have five pieces of their own color to form an unbroken line horizontally (`examples/ex1.png`), vertically (`examples/ex2.png`), or diagonally (`examples/ex3.png`). Of course, these are unlikely realistic games between reasonable players. A real game is more like `examples/ex4.png` (black is still very lame in the end).  
- The game engine starts with human against a random-play agent. Click any grid intersections and see what the computer does. Press enter to see a random game between two random-play agents (also press enter to pause autoplay and switch back to human vs random). Press 'm' to switch to manually playing both sides.  


- Functionality 

In the starter code, the automated game (press Enter) is played between two random-play agents. I changed the second player of them to an MCTS agent (See the `Board.autoplay` function). The MCTS agent should use the standard Monte Carlo Tree Search methods and always beat the random-play agent. 


In MCTS, the standard loop exits when the "computation budget" is reached. Depending on how fast your code runs, you can put a bound on the number of iterations of the MCTS loop, so that each step by the MCTS takes less than roughly 15 seconds (just so that grading is not painful for us; no need to precisely keep track of time, just translate that to some suitable number of loops). 

A main bottleneck of performance is how many next moves you need to consider each time. It is easy to realize that all the interesting moves should be pretty close to the pieces already on the board. Thus, to accelerate search, you could limit the next moves in a small square around where the pieces of your color are. 

Read the code for the random-play agent in `randplay.py` carefully. It is more verbose than needed for a random player, just to provide hints for various functions that you might need in the MCTS code. In particular, the random rollout function in the `Randplay` class can be used in the MCTS class. 

Again, random-play agent gives a pretty low bar. Try entertaining yourself by playing against your MCTS AI and see whether it's smart enough. 


