# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    position = problem.getStartState()
    #Helps tracking witch nodes we don't have to expand again.
    visited = [position]
    #Holds the node that led us here and the movement that was used to do so.
    re_path = {position: [None, None]}
    
    frontier = util.Stack()
    #We know that there is always a way to reach our goal.
    while (not problem.isGoalState(position)) :
        #i has the position, how we got there and the cost
        for i in problem.getSuccessors(position) :
            if (i[0] not in visited) :
                frontier.push(i[0])
                re_path[i[0]] = [position, i[1]]
        position = frontier.pop()
        visited.append(position)

    #Retraces the path done to get here.
    path = []
    while (re_path[position][0] is not None) :
         path.append(re_path[position][1])
         position = re_path[position][0] 
    path.reverse()
    return path

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    position = problem.getStartState()
    
    #Holds the node that we used to come here and the direction to do that.
    re_path = {position: [None, None]}
    frontier = util.Queue()
    #We know that there is always a way to reach our goal.
    while (not problem.isGoalState(position)) :
        #i has the position, how we got there and the cost
        for i in problem.getSuccessors(position) :
            if (not re_path.has_key(i[0])) :
                frontier.push(i[0])
                re_path[i[0]] = [position, i[1]]
        position = frontier.pop()
    
    path = []
    while (re_path[position][0] is not None) :
        path.append(re_path[position][1])
        position = re_path[position][0]
    path.reverse()
    return path    

def iterativeDeepeningSearch(problem):
    """
    Start with depth = 0.
    Search the deepest nodes in the search tree first up to a given depth.
    If solution not found, increment depth limit and start over.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    """
    "*** YOUR CODE HERE ***"

    max_depth = 0
    #[(i, j), depth, cost]
    position = [problem.getStartState(), 0, 0]
    while (not problem.isGoalState(position[0])) :
        position = [problem.getStartState(), 0, 0]
        re_path = {}
        #[(i,j), dir, cost]
        re_path[position[0]] = [None, None, 0]
        frontier = util.Stack()
        frontier.push(position)

        while (not problem.isGoalState(position[0]) and not frontier.isEmpty()) :
            position = frontier.pop()

            if (position[1] < max_depth) :
                for i in problem.getSuccessors(position[0]) :
                    #falsta ver o custo
                    if (re_path.has_key(i[0])) :
                        if (re_path[i[0]][2] <= position[2] + i[2]) :
                            continue

                    re_path[i[0]] = [position[0], i[1], position[2] + i[2]]
                    frontier.push([i[0], position[1] + 1, position[2] + i[2]])


        max_depth += 1

    stack = util.Stack()
    position = position[0]
    while (re_path[position][0] is not None) :
        stack.push(re_path[position][1])
        position = re_path[position][0]
    path = []
    while (not stack.isEmpty()) :
        path.append(stack.pop())
    return path

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    re_path = {}
    position = [problem.getStartState(), 0]
    frontier = util.PriorityQueue()
    re_path[position[0]] = (None, None, 0)
    while (not problem.isGoalState(position[0])) :
        for i in problem.getSuccessors(position[0]) :
            if (re_path.has_key(i[0]) and re_path[i[0]][2] <= position[1] + i[2]) :
                continue
            frontier.push([i[0], position[1] + i[2]], position[1] + i[2] + heuristic(i[0], problem))
            re_path[i[0]] = (position[0], i[1], position[1] + i[2])
        position = frontier.pop()

    stack = util.Stack()
    position = position[0]
    while (re_path[position][0] is not None) :
        stack.push(re_path[position][1])
        position = re_path[position][0]
    path = []
    while (not stack.isEmpty()) :
        path.append(stack.pop())
    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch
