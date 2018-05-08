# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = 1

        if (currentGameState.getNumFood() > successorGameState.getNumFood()) :
            score += 8

        alpha = currentGameState.getFood()
        beta = successorGameState.getFood()
        distFood1 = 0
        distFood2 = 0
        for i in range(alpha.width) :
            for j in range(alpha.height) :
                if(alpha[i][j]) :
                    distFood1 += manhattanDistance((i,j), currentGameState.getPacmanPosition())
        for i in range(beta.width) :
            for j in range(beta.height) :
                if(beta[i][j]) :
                    distFood2 += manhattanDistance((i,j), successorGameState.getPacmanPosition())

        if (distFood2 < distFood1) :
            score += 5

        for i in newGhostStates :
            gosPos = i.getPosition()
            if (manhattanDistance(gosPos, newPos) == 1) :
                score -= 10

        if (successorGameState.isLose()) :
            score = -5000
        if (successorGameState.isWin()) :
            socre = 5000

        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        value = float("-inf")
        action = None
        for a in gameState.getLegalActions(0) :
            temp = self.mimValue(gameState.generateSuccessor(0, a), 0, 1)
            if (temp > value) :
                value = temp
                action = a

        return action

    def maxValue(self, curGameState, curDepth) :
        if (curDepth == self.depth or curGameState.isWin() or curGameState.isLose()) :
            return self.evaluationFunction(curGameState)

        value = float("-inf")

        for action in curGameState.getLegalActions(0) :
            a = self.mimValue(curGameState.generateSuccessor(0, action), curDepth, 1)
            value = max(value, a)
        return value

    def mimValue(self, curGameState, curDepth, ghostNum) :
        if (curDepth == self.depth or curGameState.isWin() or curGameState.isLose()) :
            return self.evaluationFunction(curGameState)

        value = float("inf")

        for action in curGameState.getLegalActions(ghostNum) :
            if (ghostNum == curGameState.getNumAgents() - 1) :
                value = min(value, self.maxValue(curGameState.generateSuccessor(ghostNum, action), curDepth + 1))

            else :
                value = min(value, self.mimValue(curGameState.generateSuccessor(ghostNum, action), curDepth, ghostNum + 1))

        return value

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        value = float("-inf")
        alpha = float("-inf")
        beta =  float("inf")
        action = None
        for a in gameState.getLegalActions(0) :
            temp = self.mimValue(gameState.generateSuccessor(0, a), 0, 1, alpha, beta)
            if (temp > value) :
                value = temp
                action = a

            if (value > beta) :
                return value
            alpha = max(alpha, value)

        return action

    def maxValue(self, curGameState, curDepth, alpha, beta) :
        if (curDepth == self.depth or curGameState.isWin() or curGameState.isLose()) :
            return self.evaluationFunction(curGameState)

        value = float("-inf")

        for action in curGameState.getLegalActions(0) :
            temp = self.mimValue(curGameState.generateSuccessor(0, action), curDepth, 1, alpha, beta)
            value = max(value, temp)
            if (value > beta) :
                return value
            alpha = max(alpha, value)

        return value

    def mimValue(self, curGameState, curDepth, ghostNum, alpha, beta) :
        if (curDepth == self.depth or curGameState.isWin() or curGameState.isLose()) :
            return self.evaluationFunction(curGameState)

        value = float("inf")

        for action in curGameState.getLegalActions(ghostNum) :
            if (ghostNum == curGameState.getNumAgents() - 1) :
                value = min(value, self.maxValue(curGameState.generateSuccessor(ghostNum, action), curDepth + 1, alpha, beta))
            else :
                value = min(value, self.mimValue(curGameState.generateSuccessor(ghostNum, action), curDepth, ghostNum + 1, alpha, beta))

            if (value < alpha) :
                return value
            beta = min(beta, value)

        return value


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        value = float("-inf")
        action = None
        for a in gameState.getLegalActions(0) :
            temp = self.mimValue(gameState.generateSuccessor(0, a), 0, 1)
            if (temp > value) :
                value = temp
                action = a

        return action

    def maxValue(self, curGameState, curDepth) :
        if (curDepth == self.depth or curGameState.isWin() or curGameState.isLose()) :
            return self.evaluationFunction(curGameState)

        value = float("-inf")

        for action in curGameState.getLegalActions(0) :
            a = self.mimValue(curGameState.generateSuccessor(0, action), curDepth, 1)
            value = max(value, a)
        return value

    def mimValue(self, curGameState, curDepth, ghostNum) :
        if (curDepth == self.depth or curGameState.isWin() or curGameState.isLose()) :
            return float(self.evaluationFunction(curGameState))

        value = 0

        for action in curGameState.getLegalActions(ghostNum) :
            if (ghostNum == curGameState.getNumAgents() - 1) :
                value += self.maxValue(curGameState.generateSuccessor(ghostNum, action), curDepth + 1)

            else :
                value += self.mimValue(curGameState.generateSuccessor(ghostNum, action), curDepth, ghostNum + 1)

        return value / float(len(curGameState.getLegalActions(ghostNum)))


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    score = 0

    if currentGameState.isWin() :
        return float("inf")
    if currentGameState.isLose() :
        return float("-inf")

    alpha =  currentGameState.getFood()
    for i in range(alpha.width) :
        for j in range(alpha.height) :
            if(alpha[i][j]) :
                score += 1.0 / manhattanDistance((i,j), currentGameState.getPacmanPosition())

    beta = currentGameState.getNumFood()
    score += 10000000.0 / beta

    gama = 0
    for i in currentGameState.getGhostPositions() :
        if (manhattanDistance(i, currentGameState.getPacmanPosition()) <= 2) :
            gama -= 100
    score += gama


    ghostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    for i in ScaredTimes :
        score += i

    #score += currentGameState.getScore()

    return float(score)

# Abbreviation
better = betterEvaluationFunction
