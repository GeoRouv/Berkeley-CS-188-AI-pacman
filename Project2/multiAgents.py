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

        distanceFromFoodToPacman = []
        foodList = currentGameState.getFood().asList()
        pacmanPosition = list(successorGameState.getPacmanPosition())

        if action == 'Stop':
            return -float("inf")

        for ghostState in newGhostStates:
            if ghostState.scaredTimer is 0 and ghostState.getPosition() == tuple(pacmanPosition):
                return -float("inf") 

        for food in foodList:   #Calculating distance from food dots to pacman position and storing them
            x = -1*abs(food[0] - pacmanPosition[0])
            y = -1*abs(food[1] - pacmanPosition[1])
            distanceFromFoodToPacman.append(x+y) 

        return max(distanceFromFoodToPacman) #Returning maximum distance
        
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
        self.index = 0 #Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def miniMax(self, gameState, depth, agentIndex=0):
 
        if gameState.isWin() or gameState.isLose() or depth == 0:        #checking if game ends, or depth is reached
            return ( self.evaluationFunction(gameState), )               #if yes,returning current score..

        numAgents = gameState.getNumAgents()

        if agentIndex != numAgents - 1:        #if current agent is the last, decrease the depth
            newDepth = depth
        else:
            newDepth = depth - 1

        newAgentIndex = (agentIndex + 1) % numAgents

        # for each legal action store in actionList (states(succ,depth,index),actions)
        actionList = [ (self.miniMax(gameState.generateSuccessor(agentIndex, a),newDepth, newAgentIndex)[0], a) for a in gameState.getLegalActions(agentIndex)]

        if(agentIndex == 0):    #max node
            return max(actionList) #return action for max score
        else:                   #min node
            return min(actionList)  #return action for min score

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
        return self.miniMax(gameState, self.depth)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        total_agents = gameState.getNumAgents()

        def computeMax(gamestate, curr_depth, alpha, beta):
            pacman_actions = gamestate.getLegalActions(0)

            if curr_depth > self.depth or gamestate.isWin() or not pacman_actions: #if depth is reached or game is won or there are no actions for pacman then return score and stop
                return self.evaluationFunction(gamestate), Directions.STOP

            v = float('-inf')
            bestAction = Directions.STOP

            for action in pacman_actions: 
                successor = gamestate.generateSuccessor(0, action)
                cost = computeMin(successor, 1, curr_depth, alpha, beta)[0]
                if cost > v:
                    v = cost
                    bestAction = action
                if v > beta:
                    return v, bestAction
                alpha = max(alpha, v)

            return v, bestAction

        def computeMin(gamestate, agent_index, curr_depth, alpha, beta):
            ghost_actions = gamestate.getLegalActions(agent_index)
            
            if not ghost_actions or gamestate.isLose():
                return self.evaluationFunction(gamestate), Directions.STOP

            v = float('inf')
            bestAction = Directions.STOP
            PacmanFlag = agent_index == total_agents - 1
 
            for action in ghost_actions:
                successor = gamestate.generateSuccessor(agent_index, action)

                if PacmanFlag: #if pacman is next send him the score
                    cost = computeMax(successor, curr_depth + 1, alpha, beta)[0]
                else:
                    cost = computeMin(successor, agent_index + 1, curr_depth, alpha, beta)[0]

                if cost < v:
                    v = cost
                    bestAction = action
                if v < alpha:
                    return v, bestAction
                beta = min(beta, v)

            return v, bestAction


        defaultAlpha = float('-inf') #initializing alpha-beta
        defaultBeta = float('inf')

        return computeMax(gameState, 1, defaultAlpha, defaultBeta)[1] #Returns best action         
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
        
        total_agents = gameState.getNumAgents()

        def computeMax(gamestate, curr_depth):
            pacman_actions = gamestate.getLegalActions(0)

            if curr_depth > self.depth or gamestate.isWin() or not pacman_actions:
                return self.evaluationFunction(gamestate), None

            succ_score = []
            for action in pacman_actions:
                successor = gamestate.generateSuccessor(0, action)
                succ_score.append((computeMin(successor, 1, curr_depth)[0], action))

            return max(succ_score)

        def computeMin(gamestate, agent_index, curr_depth):
            ghost_actions = gamestate.getLegalActions(agent_index)

            if not ghost_actions or gamestate.isLose(): #if there are no actions for ghost or game is lost, return score
                return self.evaluationFunction(gamestate), None

            successors = [gamestate.generateSuccessor(agent_index, action) for action in ghost_actions]

            succ_score = []
            PacmanFlag = agent_index == total_agents - 1

            for successor in successors:
                if PacmanFlag:
                    succ_score.append(computeMax(successor, curr_depth + 1))
                else:
                    succ_score.append(computeMin(successor, agent_index + 1, curr_depth))

            averageScore = sum(map(lambda x: float(x[0]) / len(succ_score), succ_score)) #Return the average value so MAX evaluate it accordingly
            return averageScore, None

        return computeMax(gameState, 1)[1]

        
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: 
         
        The function created here is a linear combination of the following features.

        Evaluating according to: 
        ~distance to nearest food
        ~Closest Ghost
        ~Number of capsules on the grid
        ~Number of current scared ghosts 
        ~Current score
        
    """
    "*** YOUR CODE HERE ***"
     
    pos = currentGameState.getPacmanPosition()
    currentScore = scoreEvaluationFunction(currentGameState)
    if currentGameState.isLose(): 
        return -float("inf")
    elif currentGameState.isWin():
        return float("inf")
    
    foodlist = currentGameState.getFood().asList()  
    distToClosestFood = min(map(lambda x: util.manhattanDistance(pos, x), foodlist)) # distance to closest food dot

    FoodLeft = len(foodlist)                           # number of foods left
    CapsulesLeft = len(currentGameState.getCapsules()) #number of capsules left      
    scaredGhosts = [] #Lit
    Ghosts = []
   
    def getManhattanDistances(ghosts):  #Manhattan distances to ghosts 
      return map(lambda g: util.manhattanDistance(pos, g.getPosition()), ghosts)        

    for ghost in currentGameState.getGhostStates(): #Compute number of ghosts and scared ghosts
      if not ghost.scaredTimer:
        Ghosts.append(ghost)
      else: 
        scaredGhosts.append(ghost)

    distToClosestGhost = 0
    distToClosestScaredGhost = 0

    #Finding distance to closest ghost and closest scared ghost#
    if Ghosts:  
        distToClosestGhost = min(getManhattanDistances(Ghosts)) 
    else: 
        distToClosestGhost = float("inf")
        
    if scaredGhosts:
        distToClosestScaredGhost = min(getManhattanDistances(scaredGhosts))
    else:
        distToClosestScaredGhost = 0 #if there aren't any scared ghosts set it to 0

    '''    
           WEIGHTS OF EVALUATION VARIABLES (The greater the weight , the more important the feature is):
           
           number of capsules left          => -100 * CapsulesLeft                [Pacman should always move towards capsules instead of or running away from ghosts thats why the large multiplier]
           number of total food dots left   => -50    * (FoodLeft)                [The more food is left on the grid , the more negative the score is 
           distance to closest food         => -1 * distToClosestFood           [the larger the distance between pacman and the closest food, the more negative the score is]
           distance to closest active ghost => -2    * (1./distToClosestGhost)    [the larger the distance to the closest active ghost, the less negative the score is, but the closer a ghost is,the more negative the score becomes.  
           distance to closest scared ghost => -2    * distToClosestScaredGhost
                                  
    '''
    
    score = currentScore -100*CapsulesLeft -50*FoodLeft -1*distToClosestFood -2*(1./distToClosestGhost) -2*distToClosestScaredGhost #Linear combination of features above
    return score		

    util.raiseNotDefined()        

# Abbreviation
better = betterEvaluationFunction

