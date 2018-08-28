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
    from util import Stack

    #print "Start:", problem.getStartState()    
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())
    
    Frontier=util.Stack()
    Explored_set = []

    pathlist = []
    Frontier.push((problem.getStartState(),pathlist))   #pushing the first node ( a tuple containing the start_state ande the actions made 'till here)

    while Frontier:
    
        state,actions_made = Frontier.pop()
        
        if problem.isGoalState(state):                  #if state is goal state return the actions made 'till here
            return actions_made
        
        if state not in Explored_set:                   #if state-node is not visited yet , do it
            Explored_set.append(state)                  #include from on visited set    
            for succ in problem.getSuccessors(state):   #Getting succesors..
                if succ[0] not in Explored_set:         
                    Frontier.push( ( succ[0], actions_made+[succ[1]] ) ) #push successors in stack if not visited  


    return []
    util.raiseNotDefined()
  
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue    
    Frontier=Queue()
    Explored_set = []

    pathlist = []
    Frontier.push((problem.getStartState(),pathlist))

    while Frontier:
    
        state,actions_made = Frontier.pop()
        Explored_set.append(state)

        if problem.isGoalState(state):
            return actions_made
        
        for succ in problem.getSuccessors(state): 
            if succ[0] not in Explored_set:
                Explored_set.append(succ[0])
                Frontier.push((succ[0],actions_made+[succ[1]]))  

    return []
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue  
    Frontier=PriorityQueue()
    Explored_set = []

    pathlist = []
    Frontier.push((problem.getStartState(),pathlist),0)

    while Frontier:
    
        state,actions_made = Frontier.pop()
         
        if problem.isGoalState(state):
            return actions_made
     
        if state not in Explored_set:
            Explored_set.append(state)        
            for succ in problem.getSuccessors(state): 
                if succ[0] not in Explored_set:
                    Frontier.push((succ[0],actions_made+[succ[1]]),problem.getCostOfActions(actions_made+[succ[1]]))  #pushing successors and the whole cost of actions made till here

    return []
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
    from util import PriorityQueue  
    Frontier=PriorityQueue()
    Explored_set = []

    pathlist = []
    Frontier.push((problem.getStartState(),pathlist),0)

    while not (Frontier.isEmpty()):
    
        state,actions_made = Frontier.pop()

        if problem.isGoalState(state):
            return actions_made
      
        if state not in Explored_set:
            Explored_set.append(state)   
            for succ in problem.getSuccessors(state): 
                if succ[0] not in Explored_set: #if state not visited then
                    Frontier.push( (succ[0],actions_made+[succ[1]]) , problem.getCostOfActions(actions_made+[succ[1]]) + heuristic(succ[0],problem) )  #pushing successors and the whole cost of actions made till here+heuristic value

    
    return []
    util.raiseNotDefined()



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
