'''
    Defines Minimax algorithm
'''

from othello_board import OthelloBoard

class Minimax:
    def __init__(self):
        pass

    # returns all valid moves as a list of tupples
    def find_successors(self, board, symbol):
        successors = []
        for row in range(board.rows):
            for col in range(board.cols):
                if board.is_legal_move(col, row, symbol):
                    successors.append((col, row))
        return successors
    
    # returns the utility of a board state, defined as the number of the player's symbols on the board minus the opponents
    # derived from game_driver's winner calculation
    def find_utility(self, board, symbol, oppSym):
        utility = 0
        for row in range(board.rows):
            for col in range(board.cols):
                if board.grid[row][col] == symbol:
                    utility += 1
                elif board.grid[row][col] == oppSym:
                    utility -= 1
        return utility
    
    # Recursively finds the least worst possible scenario
    # Base case, allows infinite depth search with negative depth
    # notable additionions from GPT: added alpha beta cutoff and corrected a 'cannot unpack non-iterable NoneType object' I couldn't figure out.
    # things changed after chatgpt: fixed the return functions, fixed base case
    def minimax(self, board, depth, maximizingPlayer, symbol, oppSym, alpha=-999, beta=999):
        if depth == 0 or (not board.has_legal_moves_remaining(symbol) and not board.has_legal_moves_remaining(oppSym)):
            return (-1, -1), self.find_utility(board, symbol, oppSym)

        if maximizingPlayer:
            player_symbol = symbol
            value = -999
            best_move = ()
            successors = self.find_successors(board, player_symbol)

            for successor in successors:
                new_board = board.clone_of_board()
                new_board.play_move(successor[0], successor[1], player_symbol)

                _, successor_value = self.minimax(new_board, depth - 1, False, symbol, oppSym, alpha, beta)
                if successor_value >= value:
                    value = successor_value
                    best_move = successor
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Beta cut-off
            return best_move, value
                
        else:
            player_symbol = oppSym
            value = 999
            best_move = ()
            successors = self.find_successors(board, player_symbol)

            for successor in successors:
                new_board = board.clone_of_board()
                new_board.play_move(successor[0], successor[1], player_symbol)
                
                _, successor_value = self.minimax(new_board, depth - 1, True, symbol, oppSym, alpha, beta)
                if successor_value <= value:
                    value = successor_value
                    best_move = successor
                beta = min(beta, value)
                if alpha >= beta:
                    break  # Alpha cut-off
            return best_move, value
