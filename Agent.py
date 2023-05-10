from Tile import Tile


class Agent:
    MIN_VALUE = -1000000
    MAX_VALUE = 1000000

    def __init__(self, game, color, max_depth):
        self.game = game
        self.color = color
        self.max_depth = max_depth

    def do_min_max(self, current_board):
        move, value = self.max(current_board, self.color, 0, Agent.MIN_VALUE, Agent.MAX_VALUE)

        return move

    def max(self, current_board, current_color, depth, alpha, beta):
        if depth == self.max_depth or self.game.check_terminal(current_board, current_color):
            return None, self.game.evaluate(current_board, current_color)

        best_move = None
        value = Agent.MIN_VALUE
        valid_moves = self.game.generate_all_possible_moves(current_board, current_color)

        for move in valid_moves:
            new_board = current_board.next_board(current_color, move)
            _, new_value = self.min(new_board, self.game.opponent(current_color), depth + 1, alpha, beta)
            if new_value > value:
                best_move = move
                value = new_value
            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return best_move, value

    def min(self, current_board, current_color, depth, alpha, beta):
        if depth == self.max_depth or self.game.check_terminal(current_board, current_color):
            return None, self.game.evaluate(current_board, current_color)

        best_move = None
        value = Agent.MAX_VALUE
        valid_moves = self.game.generate_all_possible_moves(current_board, current_color)

        for move in valid_moves:
            new_board = current_board.next_board(current_color, move)
            _, new_value = self.max(new_board, self.game.opponent(current_color), depth + 1, alpha, beta)
            if new_value < value:
                best_move = move
                value = new_value
            beta = min(beta, value)
            if beta <= alpha:
                break

        return best_move, value
