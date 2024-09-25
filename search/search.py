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
    def __init__(self, state, parent, direction, cost=0):
        self.state = state
        self.parent = parent
        self.direction = direction
        self.cost = cost
    def __getitem__(self,key):
        if key == 0:
            return self.cost
        elif key == 1:
            return self.direction
        elif key == 2:
            return self.cost
        else:
            print("error, tried to get the ", key, " item in a node. Not defined.")
            return False
        
        
        


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


def genericSearch1(problem, i):
    """Search deepest node first (dfs) if i is 1 else it searches the shallowest node first (bfs)."""

    if i is 1:
        open = util.Stack()  # Stores states that need to be expanded for dfs.
        currentPath = util.Stack()  # Stores path of expanded states for dfs.
    else:
        open = util.Queue()  # Stores states that need to be expanded for bfs.
        currentPath = util.Queue()  # Stores path of expanded states for bfs.

    closed = []  # Stores states that have been expanded.
    finalPath = []  # Store final path of states.
    open.push(problem.getStartState())
    currState = open.pop()  # Current State.
    while not problem.isGoalState(currState):   # Search until goal state.

        if currState not in closed:  # New state found.
            closed.append(currState)  # Add state to closed.
            for successor in problem.getSuccessors(currState):  # Adding successors of current state.
                open.push(successor[0])  # Add to open.
                currentPath.push(finalPath + [successor[1]])  # Store path.

        currState = open.pop()  # Update current State.
        finalPath = currentPath.pop()  # Add to final path.
    return finalPath


def dfsHelper(visitedNodes, node, problem):
    node_in_visitedNodes = False
    for i in visitedNodes:
        if i.state == node.state:
            node_in_visitedNodes = True
    if not node_in_visitedNodes:
        #print(visitedNodes)
        visitedNodes.add(node)
        for n in problem.getSuccessors(node.state):
            child = Node(n[0], node, None)
            dfsHelper(visitedNodes, child, problem)



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



    return genericSearch1(problem, 1)




    visitedNodes = set()
    dfsHelper(visitedNodes, Node(problem.getStartState(), None, None), problem)
    order = []
    for i in visitedNodes:
        if problem.isGoalState(i.state):
            p = i
            while p is not None:
                order.append(p)
                p = p.parent
    order = order[::-1] #reverse order
    path = []
    for i in range(len(order)):
        if i+1 > len(order)-1:
            break
        else:
            for j in problem.getSuccessors(order[i].state):
                if j[0] == order[i+1].state:
                    if j[1] == "North":
                        path.append(Directions.NORTH)
                    elif j[1] == "South":
                        path.append(Directions.SOUTH)
                    elif j[1] == "East":
                        path.append(Directions.EAST)
                    elif j[1] == "West":
                        path.append(Directions.WEST)
                    
    return path

    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())
    util.raiseNotDefined()

def bfsHelper(problem):
    from util import Queue
    """Search the shallowest nodes in the search tree first."""
    node = Node(problem.getStartState(), None, None)
    if problem.isGoalState(node.state):
        return node
    frontier = Queue()
    frontier.push(node)
    reached = [problem.getStartState()]
    while not frontier.isEmpty():
        node = frontier.pop()
        for i in problem.getSuccessors(node.state):
            s = i[0]
            if problem.isGoalState(s):
                newNode = Node(i[0], node, i[1])
                return newNode
            if not s in reached:
                newNode = Node(i[0], node, i[1])
                frontier.push(newNode)
                reached.append(s)
    print(frontier)
    print(reached)

def breadthFirstSearch(problem):
    return genericSearch1(problem, 2)
    from game import Directions
    path = []
    node = bfsHelper(problem)
    if node:
        while node.parent is not None:
            if node.direction == "North":
              path.append(Directions.NORTH)
            elif node.direction == "South":
                path.append(Directions.SOUTH)
            elif node.direction == "East":
                path.append(Directions.EAST)
            elif node.direction == "West":
                path.append(Directions.WEST)
            
            node = node.parent
    return path[::-1] #reverse order


    util.raiseNotDefined()
# REFRENCE: https://github.com/nomaanakhan/Berkeley-AI-Pacman-Search/blob/master/search/search.py#L141
# this code is a modified version of the above link, as I was completely stuck and the textbook didn't mention the getCostOfActions function.
def genericSearch(problem, heuristic):
    open = util.PriorityQueue()  # Stores nodes that need to be expanded for Uniform Cost Search.
    currPath = util.PriorityQueue()  # Stores path of expanded states.
    expandedStates = []  # Stores states that have been expanded.
    finalPath = []  # Store final path of nodes.
    node = Node(problem.getStartState(), None, None, 0)
    open.push(node, node.cost)
    currNode = open.pop()  # Current Node.
    while not problem.isGoalState(currNode.state):  # Search until goal state.
        if currNode.state not in expandedStates:  # New state found.
            expandedStates.append(currNode.state)  # Add state to closed.

            for successor in problem.getSuccessors(currNode.state):  # To calculate costs of successors of current node's state.
                newNode = Node(successor[0], node, successor[1], successor[2])
                pathCost = problem.getCostOfActions(finalPath + [newNode.direction])  # Cost of selecting successor.
                if heuristic is not None:  # Add heuristic if A* search.
                    pathCost += heuristic(newNode.state, problem)
                if newNode.state not in expandedStates:  # If successor is a new state add to open queue and store path.
                    open.push(newNode, pathCost)
                    currPath.push(finalPath + [newNode.direction], pathCost)

        currNode = open.pop()  # Update current state.
        finalPath = currPath.pop()  # Add to final path.
    
    print(currPath)
    return finalPath

""" BROKEN
def bestFirstSearch(problem):
    from util import Queue
    node = Node(problem.getStartState(), None, None, 0)
    frontier = util.PriorityQueueWithFunction(problem.costFn)
    frontier.push(node)
    reached = {problem.getStartState(): node}
    while (not frontier.isEmpty()):
        node = frontier.pop()
        if problem.isGoalState(node.state):
            return node
        
        for child in problem.getSuccessors(node.state):
            newNode = Node(child[0], node, child[1])
            s = newNode.state
            if not s in reached.keys() or newNode.cost < reached[s].cost:
                reached[s] = newNode
                frontier.push(newNode)
    return False #failure
"""           

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
