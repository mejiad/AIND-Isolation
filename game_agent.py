"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """

    # TODO: finish this function!
    # primer intento, regresar le numero de posiciones abiertas para el player...
    # raise NotImplementedError
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        # print("get_move iself.iterative: ", self.iterative, " method:", self.method, " Legal moves:", legal_moves)
        #print("Get Move game agent")
        posAnterior = (-1,-1)
        is_maximizing = True
        if (game.active_player == game.__player_1__):
            is_maximizing = True
        else:
            is_maximizing = False

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if self.iterative == True:
                depth = 1
                for depth in range(1, 8):
                    if (self.method == "minimax"):
                        score, pos =  self.minimax(game, depth, True)
                    else: 
                        score, pos =  self.alphabeta(game, depth, float("-inf"), float("inf"), is_maximizing)
                    if(pos == (-1,-1)):
                        # print("Sali antes:" , self.method )
                        return posAnterior
                    posAnterior = pos
            else:
                if (self.method == "minimax"):
                    score, pos = self.minimax(game, self.search_depth, is_maximizing)
                else:
                    score, pos =  self.alphabeta(game,  self.search_depth, float("-inf"), float("inf"), is_maximizing)
                posAnterior = pos

        except Timeout:
            # Handle any actions required at timeout, if necessary
            # print("PostAnterior timeout ", posAnterior, flush = True)
            return posAnterior

        # Return the best move from the last completed search iteration
        # print("PostAnterior ret:", posAnterior)
        return posAnterior

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)
        if (game.utility(game.active_player)):
            print("minimax debe salir!")
            return  game.utility(game.active_player), (-1,-1)
        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        # raise NotImplementedError
        # print("<<<<<<<<<<< Minimax 1 depth:", depth)
        # print( game.print_board2(depth))
        moves = game.get_legal_moves() 
        # print("fepth:", depth, " Moves en minimax:", moves)

        # if (len(moves) == 1) :
            # return self.score(game,game.__player_1__), moves[0]

        if (len(moves) < 1) :
            if ( maximizing_player == True) :
                return float("-inf"),  (-1,-1)
            else:
                return float("inf"),  (-1,-1)

        # Determine if the limit of search has been reached, or if the 
        # level is a minimizing level, or if the level is a maximizing
        # level:
        # 1a. If the limit of search has been reached, compute the
        #     static value of the current position relative to the 
        #     appropiate player. Report the result
        # 1b  If the level is a minimizing level, use MINIMAX on the
        #     children of the current position. Report the minimun
        #     of the result.
        # 1c  Otherwise, the level is maximizing level. use MINIMAX
        #     on the children of the current position. Report 
        #     the maximun of the result.
        # print("Movimientos: ", moves)
        # print("Utility: " , game.utility(game.active_player) )

        # Determine if the limit of search has been reached
        # se alcanza si depth == 1, ya llegamos al final del arbol
        # o si no hay movimientos para este nivel...
        # if (game.utility(game.active_player) != 0):
            # print("------------- minimax SALIO   ",  game.utility(game.active_player))
            # return  game.utility(game.active_player), (-1,-1)

        ret = float("inf")
        movRet = (-1, -1)
        if (depth == 1):
            if(maximizing_player == True):
                ret = float("-inf")
            else:
                ret = float("inf")
            movRet = (-1, -1)
            for move in moves:
                nuevo_tablero = game.forecast_move(move)
                score = self.score(nuevo_tablero,game.__player_1__)
                # score = self.score(nuevo_tablero,nuevo_tablero.active_player)
                # print("Score depth 1:", score)
                if (maximizing_player == True):
                    if (score > ret ):
                        ret = score
                        movRet = move
                else:
                    if (score < ret ):
                        ret = score
                        movRet = move
        else:
            # 1b  If the level is a minimizing level, use MINIMAX on the
            # checar si es minimax level
            if(maximizing_player == True):
                ret = float("-inf")
            else:
                ret = float("inf")
            movRet = (-1, -1)
            for move in moves:
                nuevo_tablero = game.forecast_move(move)
                score, movTemp = self.minimax(nuevo_tablero, depth-1, not maximizing_player) 
                # print("Score depth 2:", score)
                if(maximizing_player == True):
                    if (score > ret ):
                        ret = score
                        movRet = move
                else:
                    if (score < ret ):
                        ret = score
                        movRet = move

        return ret, movRet

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()


        # TODO: finish this function!
        # raise NotImplementedError

        
        # TODO: finish this function!
        # raise NotImplementedError
        # print("------------- alphabeta")
        # print("<<<<<<<<<<< Alpha-beta 1 depth:", depth)

        # print( game.print_board())
        moves = game.get_legal_moves(game.active_player) 

        # Determine if the limit of search has been reached, or if the 
        # level is a minimizing level, or if the level is a maximizing
        # level:
        # 1a. If the limit of search has been reached, compute the
        #     static value of the current position relative to the 
        #     appropiate player. Report the result
        # 1b  If the level is a minimizing level, use MINIMAX on the
        #     children of the current position. Report the minimun
        #     of the result.
        # 1c  Otherwise, the level is maximizing level. use MINIMAX
        #     on the children of the current position. Report 
        #     the maximun of the result.
        # print("AB Movimientos: ", moves)


        # TODO: agregar utility
        # if (game.utility(game.active_player) != 0):
            # print("------------- alphabeta SALIO depth: ", depth, " moves:",  moves)
            # return  game.utility(game.active_player), (-1,-1)

        # if (len(moves) == 1) :
            # return self.score(game,game.__player_1__), moves[0]

        if (len(moves) < 1) :
            if ( maximizing_player == True) :
                return float("-inf"),  (-1,-1)
            else:
                return float("inf"),  (-1,-1)

        # Determine if the limit of search has been reached
        # se alcanza si depth == 1, ya llegamos al final del arbol
        # o si no hay movimientos para este nivel...
        
        ret = float("inf")
        movRet = (-1, -1)
        if (depth == 1):
            # ya llegamos al final
            if(maximizing_player == True):
                ret = float("-inf")
            else:
                ret = float("inf")
            movRet = (-1, -1)
            for move in moves:
                nuevo_tablero = game.forecast_move(move)
                score = self.score(nuevo_tablero, game.__player_1__)
                if (maximizing_player == True):
                    if (score > ret ):
                        ret = score
                        movRet = move
                    if (ret > alpha):
                        alpha = ret
                else:
                    if (score < ret ):
                        ret = score
                        movRet = move
                    if(ret < beta) :
                        beta = ret
                if (maximizing_player == True):
                    if (alpha >= beta) :
                        return alpha, move
                else:
                    if (alpha >= beta) :
                        return beta, move

        else:
            # 1b  If the level is a minimizing level, use MINIMAX on the
            # checar si es minimax level
            # print("Alpha-Beta depth > 1: ", depth)
            if(maximizing_player == True):
                ret = float("-inf")
            else:
                ret = float("inf")
            movRet = (-1, -1)
            for move in moves:
                nuevo_tablero = game.forecast_move(move)
                score, movTemp = self.alphabeta(nuevo_tablero, depth-1, alpha, beta, not maximizing_player) 
                # if(movTemp == (-1,-1)):
                    # print("Si fue -1,-1 depth:", depth)
                    # return score, movTemp
                if(maximizing_player == True):
                    if (score > ret ):
                        ret = score
                        movRet = move
                    if (ret > alpha):
                        alpha = ret
                else:
                    if (score < ret ):
                        ret = score
                        movRet = move
                    if(ret < beta) :
                        beta = ret
                if (maximizing_player == True):
                    if (alpha >= beta) :
                        return alpha, move
                else:
                    if (alpha >= beta) :
                        return beta, move

        return ret, movRet

