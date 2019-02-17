
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition or self.currentState not in self.visited:
            self.visited[self.currentState] = True
            return self.currentState.state == self.victoryCondition

        if self.currentState.nextChildToVisit==0: # first time to visit the state; expand it 
            for movable in self.gm.getMovables():
                self.gm.makeMove(movable)
                newState = self.gm.getGameState()
                newGameState = GameState(newState, self.currentState.depth+1, movable)  
                if newGameState not in self.visited:
                    newGameState.parent = self.currentState
                    self.currentState.children.append(newGameState)
                self.gm.reverseMove(movable)            

        if self.currentState.nextChildToVisit<len(self.currentState.children):
            newState = self.currentState.children[self.currentState.nextChildToVisit]
            self.currentState.nextChildToVisit += 1
            self.gm.makeMove(newState.requiredMovable)
            self.currentState = newState
            return self.solveOneStep()
        else:
            self.currentState.nextChildToVisit += 1
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return self.solveOneStep()









class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
            self.visited[self.currentState] = True
            return self.currentState.state == self.victoryCondition

        depth = self.currentState.depth
        while True:
            res = self.solveOneStepDls(depth)
            if res:
                if self.currentState.state == self.victoryCondition:
                    return True
                else:
                    depth += 1
            else:
                return False





    def solveOneStepDls(self, depth):
        # return true if desired solution is reached or depth is exausted, False otherwise.
        if self.currentState.depth > depth:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return self.solveOneStepDls(depth)  
        elif self.currentState.depth == depth:
            if self.currentState not in self.visited or depth == 0 and not self.currentState.children:
                for movable in self.gm.getMovables():
                    self.gm.makeMove(movable)
                    newState = self.gm.getGameState()
                    newGameState = GameState(newState, self.currentState.depth+1, movable)  
                    if newGameState not in self.visited:
                        newGameState.parent = self.currentState
                        self.currentState.children.append(newGameState)
                    self.gm.reverseMove(movable)  

            if self.currentState.state == self.victoryCondition or self.currentState not in self.visited:
                self.visited[self.currentState] = True
                return self.currentState.state == self.victoryCondition   
            else:
                if self.currentState.depth == 0: return True
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                return self.solveOneStepDls(depth)       
        else:
            if self.currentState.nextChildToVisit > len(self.currentState.children):
                self.currentState.nextChildToVisit = 0
            if self.currentState.nextChildToVisit < len(self.currentState.children):
                newState = self.currentState.children[self.currentState.nextChildToVisit]
                self.currentState.nextChildToVisit += 1
                self.gm.makeMove(newState.requiredMovable)
                self.currentState = newState
                return self.solveOneStepDls(depth)
            else:
                self.currentState.nextChildToVisit += 1
                if self.currentState.depth == 0: return True
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                return self.solveOneStepDls(depth)        



