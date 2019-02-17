from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        gs = [[],[],[]] # game state
        lob = self.kb.kb_ask(parse_input('fact: (on ?disk ?peg)')) # list of bindings
        for binding in lob:
            gs[int(binding['?peg'][3])-1].append(int(binding['?disk'][4]))
        return tuple(map(lambda x: tuple(sorted(x)),gs))

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        sl = list(map(lambda x: str(x), movable_statement.terms))
        to_retract = [parse_input('fact: (topOf ' + sl[0] + ' ' + sl[1] + ')')]
        to_assert = [parse_input('fact: (topOf ' + sl[0] + ' ' + sl[2] + ')')]

        answer = self.kb.kb_ask(parse_input('fact: (topOf ?disk ' + sl[2] + ')'))
        if not answer: # destination empty
            to_retract.append(parse_input('fact: (empty ' + sl[2] + ')'))
            to_assert.append(parse_input('fact: (onPeg ' + sl[0] + ' ' + sl[2] + ')'))
        else:
            to_retract.append(parse_input('fact: (topOf ' + answer[0]['?disk'] + ' '+ sl[2] + ')'))
            to_assert.append(parse_input('fact: (onDisk ' + sl[0] + ' ' + answer[0]['?disk'] + ')'))

        answer = self.kb.kb_ask(parse_input('fact: (onDisk ' + sl[0] + ' ?disk)'))
        if answer: # source would not be empty
            to_retract.append(parse_input('fact: (onDisk ' + sl[0] + ' ' + answer[0]['?disk'] + ')'))
            to_assert.append(parse_input('fact: (topOf ' + answer[0]['?disk'] + ' ' + sl[1] + ')'))
        else:
            to_retract.append(parse_input('fact: (onPeg ' + sl[0] + ' ' + sl[1] + ')'))
            to_assert.append(parse_input('fact: (empty ' + sl[1] + ')'))

        for fact in to_retract:
            self.kb.kb_retract(fact)
        for fact in to_assert:
            self.kb.kb_assert(fact)




    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        gs = [[-1 for _ in range(3)] for _ in range(3)] # game state
        lob = self.kb.kb_ask(parse_input('fact: (at ?tile ?posx ?posy'))
        for bindings in lob:
            gs[int(bindings['?posy'][3])-1][int(bindings['?posx'][3])-1] = int(bindings['?tile'][4])
        return tuple(tuple(l) for l in gs)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        sl = list(map(lambda x: str(x), movable_statement.terms))
        to_retract = [parse_input('fact: (at ' + sl[0] + ' ' + sl[1] + ' ' + sl[2] + ')'), parse_input('fact: (empty ' + sl[3] + ' ' + sl[4] + ')')]
        to_assert = [parse_input('fact: (at ' + sl[0] + ' ' + sl[3] + ' ' + sl[4] + ')'), parse_input('fact: (empty ' + sl[1] + ' ' + sl[2] + ')')]

        for fact in to_retract:
            self.kb.kb_retract(fact)
        for fact in to_assert:
            self.kb.kb_assert(fact)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
