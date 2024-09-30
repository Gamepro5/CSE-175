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

class Node:
    def __init__(self, state, parent, direction, cost=0, additional_data = None):
        self.state = state
        self.parent = parent
        self.direction = direction
        self.cost = cost
        self.additional_data = additional_data
    def __iter__(self):
        return self.state
    def __getitem__(self, key):
        if key == 0:
            return self.state
        elif key == 1:
            return self.direction
        
        
        


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


# REFRENCE: https://github.com/nomaanakhan/Berkeley-AI-Pacman-Search/blob/master/search
def genericSearch1(problem, depthfirst):

    if depthfirst is True:
        open = util.Stack()  # Stores states that need to be expanded for dfs
        currentPath = util.Stack()  # Stores path of expanded states for dfs
    else:
        open = util.Queue()  # Stores states that need to be expanded for bfs
        currentPath = util.Queue()  # Stores path of expanded states for bfs

    expandedStates = []  # Stores states that have been expanded
    finalPath = []  # Store final path of states

    open.push(Node(problem.getStartState(), None, None, 0))
    currNode = open.pop()
    currState = currNode.state
    while not problem.isGoalState(currState):   # Search until goal state
        if currState not in expandedStates:  # New state found
            expandedStates.append(currState) 
            for successor in problem.getSuccessors(currState):  # Adding successors of current state
                newNode = Node(successor[0], currNode, successor[1], successor[2])
                open.push(newNode)
                currentPath.push(finalPath + [newNode.direction])  # Store path
        currNode = open.pop()
        currState = currNode.state
        finalPath = currentPath.pop()
    return finalPath



# REFRENCE: https://github.com/nomaanakhan/Berkeley-AI-Pacman-Search/blob/master/search
# this code is a modified version of the above link, as I was completely stuck and the textbook didn't mention the getCostOfActions function.
def genericSearch(problem, heuristic):
    open = util.PriorityQueue()  # Stores nodes that need to be expanded for Uniform Cost Search.
    currPath = util.PriorityQueue()  # Stores path of expanded states.
    expandedStates = []  # Stores states that have been expanded.
    finalPath = []  # Store final path of nodes.
    node = Node(problem.getStartState(), None, None, 0)
    open.push(node, node.cost)
    currNode = open.pop() 
    currState = currNode.state
    while not problem.isGoalState(currState):  # Search until goal state.
        if currState not in expandedStates:  # New state found.
            expandedStates.append(currState)
            for successor in problem.getSuccessors(currState):  # To calculate costs of successors of current node's state.
                newNode = Node(successor[0], node, successor[1], successor[2])
                pathCost = problem.getCostOfActions(finalPath + [newNode.direction])  # Cost of selecting successor.
                if heuristic is not None:  # Add heuristic if A* search.
                    pathCost += heuristic(newNode.state, problem)
                if newNode.state not in expandedStates:  # If successor is a new state add to open queue and store path.
                    open.push(newNode, pathCost)
                    currPath.push(finalPath + [newNode.direction], pathCost)  # Store path

        currNode = open.pop()
        currState = currNode.state
        finalPath = currPath.pop()
    
    print(currPath)
    return finalPath




def depthFirstSearch(problem):
    from game import Directions
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
    # uses https://favtutor.com/blogs/depth-first-search-python as refrence
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())



    return genericSearch1(problem, True)



    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())
    util.raiseNotDefined()


def breadthFirstSearch(problem):
    return genericSearch1(problem, False)
    util.raiseNotDefined()

def uniformCostSearch(problem):
    from game import Directions
    """Search the node of least total cost first."""
    return genericSearch(problem, None)
    
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
    return genericSearch(problem, heuristic)
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
