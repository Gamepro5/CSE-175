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
        #print(legalMoves)
        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        import math
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
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        food = currentGameState.getFood().asList()

        "*** YOUR CODE HERE ***"
        for ghostState in newGhostStates:
            if ghostState.getPosition() == newPos:
              return -100 #don't go there!!
        if currentGameState.getPacmanPosition() == newPos:
            return -1 #never stand still
        
        if newPos in food:
            return 1000
        
        distance = 0.0
        
        for i in newFood:
          p2 = newPos
          p1 = i
          distance += 1.0/float(abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]))
        return distance
        

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

        def terminalState(gameState, agentID, depth):
          actions=gameState.getLegalActions(agentID)
          if len(actions)==0 or gameState.isWin() or gameState.isLose() or depth==self.depth: # terminal state
              return True
          return False
        def minimax(gameState, agentID, depth):
          value, move = maxValue(gameState, agentID, depth)
          return move
        def maxValue(gameState, agentID, depth):
          if terminalState(gameState, agentID, depth):
            return(self.evaluationFunction(gameState),None)
          v = -float("inf")
          move = None
          for action in gameState.getLegalActions(agentID):
            v2, action2 = minValue(gameState.generateSuccessor(agentID,action), 1, depth)
            if v2 > v:
              v, move = v2, action
          return v, move
        def minValue(gameState, agentID, depth):
          if terminalState(gameState, agentID, depth):
            return(self.evaluationFunction(gameState),None)
          v = float("inf")
          move = None
          for action in gameState.getLegalActions(agentID):
            v2 = None
            if(agentID==gameState.getNumAgents() -1):
              v2, action2 = maxValue(gameState.generateSuccessor(agentID,action), 0, depth+1)
            else:
              v2, action2 = minValue(gameState.generateSuccessor(agentID,action), agentID+1, depth)
            if v2 < v:
              v, move = v2, action
          return v, move

        return minimax(gameState, 0, 0)
        """
        def terminalState(gameState, agentID, depth):
          actions=gameState.getLegalActions(agentID)
          if len(actions)==0 or gameState.isWin() or gameState.isLose() or depth==self.depth: # terminal state
              return True
          return False
        
        def maxValue(gameState, agentID, depth):
          if terminalState(gameState,agentID,depth): # terminal state
            return(self.evaluationFunction(gameState),None)
          v = -(float("inf")) #negative infinity
          actions=gameState.getLegalActions(agentID)
          resultAction = None
          for action in actions:
            sucsValue = minValue(gameState.generateSuccessor(agentID,action), agentID, depth+1)
            if sucsValue[0]>v:
                resultAction=action
            v=max(v,sucsValue[0])
          return (v,action)
        
        def minValue(gameState, agentID, depth):
          if terminalState(gameState,agentID,depth): # terminal state
            return(self.evaluationFunction(gameState),None)
          v = (float("inf")) #positive infinity
          actions=gameState.getLegalActions(agentID)
          resultAction = None
          for action in actions:
            sucsValue = maxValue(gameState.generateSuccessor(agentID,action), agentID, depth+1)
            if sucsValue[0]<v:
                resultAction=action
            v=min(v,sucsValue[0])
          return (v,action)

        def minimax(gameState, agentID, depth):
          return minValue(gameState,agentID,depth)
          """
        """
        def minimax(gameState, agentID, depth):
          actions=gameState.getLegalActions(agentID)
          if terminalState(gameState,agentID,depth): # terminal state
            return(self.evaluationFunction(gameState),None)
          if(agentID==gameState.getNumAgents() -1):
            v = -(float("inf")) #negative infinity
            resultAction=None
            for action in actions:
              sucsValue=minimax(gameState.generateSuccessor(agentID,action),agentID,depth + 1)
              sucsValue = sucsValue[0]
              if sucsValue<v:
                v=sucsValue
                resultAction=action
            return(v,resultAction)
          else:
            v = (float("inf")) #positive infinity
            resultAction=None
            for action in actions:
              sucsValue=minimax(gameState.generateSuccessor(agentID,action),agentID+1,depth)
              sucsValue = sucsValue[0]
              if sucsValue>v:
                v=sucsValue
                resultAction=action
            return(v,resultAction)
        
        return minimax(gameState, 0, 0)[1]
        """
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def terminalState(gameState, agentID, depth):
          actions=gameState.getLegalActions(agentID)
          if len(actions)==0 or gameState.isWin() or gameState.isLose() or depth==self.depth: # terminal state
              return True
          return False
        def minimax(gameState):
          value, move = maxValue(gameState, 0, 0, -float("inf"), float("inf"))
          return move
        def maxValue(gameState, agentID, depth, pacmanBestOption, ghostBestOption):
          if terminalState(gameState, agentID, depth):
            return(self.evaluationFunction(gameState),None)
          v = -float("inf")
          move = None
          for action in gameState.getLegalActions(agentID):
            v2, action2 = minValue(gameState.generateSuccessor(agentID,action), 1, depth, pacmanBestOption, ghostBestOption)
            if v2 > v:
              v, move = v2, action
            if v>ghostBestOption:
               return v, move
            pacmanBestOption = max(pacmanBestOption,v)
          return v, move
        def minValue(gameState, agentID, depth, pacmanBestOption, ghostBestOption):
          if terminalState(gameState, agentID, depth):
            return(self.evaluationFunction(gameState),None)
          v = float("inf")
          move = None
          for action in gameState.getLegalActions(agentID):
            v2 = None
            if(agentID==gameState.getNumAgents() -1):
              v2, action2 = maxValue(gameState.generateSuccessor(agentID,action), 0, depth+1, pacmanBestOption, ghostBestOption)
            else:
              v2, action2 = minValue(gameState.generateSuccessor(agentID,action), agentID+1, depth, pacmanBestOption, ghostBestOption)
            if v2 < v:
              v, move = v2, action
            if v<pacmanBestOption:
               return v, move
            ghostBestOption = min(ghostBestOption,v)
          return v, move

        return minimax(gameState)
        util.raiseNotDefined()

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
        def terminalState(gameState, agentID, depth):
          actions=gameState.getLegalActions(agentID)
          if len(actions)==0 or gameState.isWin() or gameState.isLose() or depth==self.depth: # terminal state
              return True
          return False
        def expectimax(gameState):
          value, move = maxValue(gameState, 0, 0)
          return move
        def maxValue(gameState, agentID, depth):
          if terminalState(gameState, agentID, depth):
            return(self.evaluationFunction(gameState),None)
          v = -float("inf")
          move = None
          for action in gameState.getLegalActions(agentID):
            v2, action2 = expecValue(gameState.generateSuccessor(agentID,action), 1, depth)
            if v2 > v:
              v, move = v2, action
          return v, move
        def expecValue(gameState, agentID, depth):
          if terminalState(gameState, agentID, depth):
            return(self.evaluationFunction(gameState),None)
          v = 0
          for action in gameState.getLegalActions(agentID):
            v2 = None
            if(agentID==gameState.getNumAgents() -1):
              v2, action2 = maxValue(gameState.generateSuccessor(agentID,action), 0, depth+1)
            else:
              v2, action2 = expecValue(gameState.generateSuccessor(agentID,action), agentID+1, depth)
            probability = v2/len(gameState.getLegalActions(agentID))
            v+=probability
          return v, None

        return expectimax(gameState)
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: I basically returned the game's score plus the general distance from the cluster of dots. I also subtracted that by the ghost's distance to ensure pacman will always be on his toes.
    """
    "*** YOUR CODE HERE ***"
  
    
    pos = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    food = currentGameState.getFood().asList()
    #print(pos, currentGameState.getScore())
    #return currentGameState.getScore()
    if currentGameState.isWin():
       return float("inf")
    
    for ghostState in ghostStates:
      if ghostState.getPosition() == pos:
          return -float("inf") #you will die. Run.

    

    smallestDistance = float("inf")
    for i in food:
      p2 = pos
      p1 = i
      distance = 1.0/float(abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]))
      if distance < smallestDistance:
         smallestDistance = distance
         


    distance = 0.0
    for i in food:
      p2 = pos
      p1 = i
      distance += 1.0/float(abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]))
    
    p1 = pos
    p2 = ghostStates[0].getPosition()
    distanceFromGhost = 1.0/float(abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]))

    score = currentGameState.getScore()
    print(score, smallestDistance, distance)
    score = score + distance - distanceFromGhost
    
    return score
    """
    distance = 0.0
    for i in food:
      p2 = pos
      p1 = i
      distance += 1.0/float(abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]))
    return distance
    """
    util.raiseNotDefined()
    
# Abbreviation
better = betterEvaluationFunction

