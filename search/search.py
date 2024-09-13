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
    def __init__(self, state, parent, direction):
        self.state = state
        self.parent = parent
        self.direction = direction
        


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
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
