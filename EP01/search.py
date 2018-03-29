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
    visited = [position]
    re_path = [(position, -1, "None")]
    frontier = util.Stack()
    while (not problem.isGoalState(position)) :
        for i in problem.getSuccessors(position) :
            if (i[0] not in visited) :
                frontier.push(i[0])
                re_path.append((i[0], visited.index(position), i[1]))
        position = frontier.pop()
        visited.append(position)

    path = util.Stack()
    i = len(re_path) - 1
    path.push(re_path[-1][2])
    while (re_path[i][1] != -1) :
        k = re_path[i][1]
        path.push(re_path[i][2])
        for j in range(len(re_path)) :
            if (visited[k] == re_path[j][0]) :
                i = j
    actions = []
    while (not path.isEmpty()) :
        actions.append(path.pop())
    return(actions[:-1])

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    position = problem.getStartState()
    visited = [position]
    re_path = [(position, -1, "None")]
    frontier = util.Queue()
    while (not problem.isGoalState(position)) :
        for i in problem.getSuccessors(position) :
            if (i[0] not in visited) :
                frontier.push(i[0])
                re_path.append((i[0], visited.index(position), i[1]))
        position = frontier.pop()
        visited.append(position)

    path = util.Stack()
    for j in range(len(re_path)) :
        if (visited[-1] == re_path[j][0]) :
            i = j
    path.push(re_path[i][2])
    while (re_path[i][1] != -1) :
        k = re_path[i][1]
        path.push(re_path[i][2])
        for j in range(len(re_path)) :
            if (visited[k] == re_path[j][0]) :
                i = j
    actions = []
    while (not path.isEmpty()) :
        actions.append(path.pop())
    return(actions[:-1])

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
    position = [problem.getStartState(), 0, 0]
    while (not problem.isGoalState(position[0])) :
        position = [problem.getStartState(), 0, 0]
        visited = []
        frontier = util.Stack()
        frontier.push(position)

        while (not problem.isGoalState(position[0]) and not frontier.isEmpty()) :
            position = frontier.pop()
            visited.append(position)

            if (position[1] < max_depth) :
                for i in problem.getSuccessors(position[0]) :
                    #ver se agente ja visitou alguem com o custo menor
                    frontier.push([i[0], position[1] + 1, position[2] + i[2]])
        print(visited)            
        max_depth += 1
    print(visited)
    util.raiseNotDefined()

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
    position = problem.getStartState()
    frontier = util.PriorityQueue()
    visited = [position]
    totCost = [0]
    while (not problem.isGoalState(position)) :
        for i in problem.getSuccessors(position) :
            if (i[0] in visited and totCost[visited.index(i[0])] < i[2]) :
                continue
            frontier.update(i[0], i[2] + heuristic(i[0], problem))
        position = frontier.pop()
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch
