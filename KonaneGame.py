from Tile import Tile

class KonaneGame:
    def __init__(self):
        self.hash_table = {}

        
    def initialize_board(self, board_size):
        board = []
        tile = Tile(2,0,0,0)
        for i in range(board_size):
            row_gui = []
            for j in range(board_size):
                row_gui.append(tile)
                tile = Tile(3-tile.piece, tile.outline, i, j+1)
            board.append(row_gui)
            if board_size%2 == 0:
                tile = Tile(3-tile.piece, tile.outline, i+1, 0)

        return board


    def generate_all_possible_moves(self, board, player):
        """
        Generates and returns all legal moves for the given player using the
        current board configuration.
        """
        if board.is_opening_move():
            if player== Tile.P_Black:
                return self.generate_first_moves(board)
            else:
                return self.generate_second_moves(board)
        else:
            moves = []
            rd = [-1,0,1,0]
            cd = [0,1,0,-1]
            for r in range(board.size):
                for c in range(board.size):
                    if board.game_board[r][c].piece == player:
                        for i in range(len(rd)):
                            moves += self.check(board, r,c,rd[i],cd[i],1,
                                                self.opponent(player))
            return moves
        

    def generate_first_moves(self, board):
        """
        Returns the special cases for the first move of the game.
        """
        moves = []
        moves.append([0]*4)
        moves.append([board.size-1]*4)
        moves.append([board.size//2]*4)
        moves.append([(board.size//2)-1]*4)
        return moves


    def generate_second_moves(self, board):
        """
        Returns the special cases for the second move of the game, based
        on where the first move occurred.
        """
        moves = []
        if board.game_board[0][0].piece == Tile.P_NONE:
            moves.append([0,1]*2)
            moves.append([1,0]*2)
            return moves
        elif board.game_board[board.size-1][board.size-1].piece == Tile.P_NONE:
            moves.append([board.size-1,board.size-2]*2)
            moves.append([board.size-2,board.size-1]*2)
            return moves
        elif board.game_board[board.size//2-1][board.size//2-1].piece == Tile.P_NONE:
            pos = board.size//2 -1
        else:
            pos = board.size//2
        moves.append([pos,pos-1]*2)
        moves.append([pos+1,pos]*2)
        moves.append([pos,pos+1]*2)
        moves.append([pos-1,pos]*2)
        return moves


    def check(self, board, r, c, rd, cd, factor, opponent):
        """
        Checks whether a jump is possible starting at (r,c) and going in the
        direction determined by the row delta (rd), and the column delta (cd).
        The factor is used to recursively check for multiple jumps in the same
        direction.  Returns all possible jumps in the given direction.
        """
        if board.contains(r+factor*rd,c+factor*cd,opponent) and \
           board.contains(r+(factor+1)*rd,c+(factor+1)*cd, Tile.P_NONE):
            return [[r,c,r+(factor+1)*rd,c+(factor+1)*cd]] + \
                   self.check(board, r,c,rd,cd,factor+2,opponent)
        else:
            return []


    def get_moves_at_tile(self, board, tile, player):
        moves =  self.generate_all_possible_moves(board, player)
        valid_moves_at_tile = []
        print(moves)
        for move in moves:
            if move[0] == tile.row and move[1] == tile.col:
                valid_tile = board.game_board[move[2]][move[3]]
                valid_moves_at_tile.append(valid_tile)
        return valid_moves_at_tile
    

    def find_winner(self, board, color):
        valid_moves = self.generate_all_possible_moves(board, color)

        if valid_moves == []:
            winner = (Tile.P_Black if color == Tile.P_White else Tile.P_White)
            return winner

    
    def check_terminal(self, board, color): 

        valid_moves = self.generate_all_possible_moves(board, color)
        return True if valid_moves == [] else False


    def opponent(self, tile):
        """
        Given a player symbol, returns the opponent's symbol, 'B' for black,
        or 'W' for white.  (3 - color)
        """
        return Tile.P_Black if tile == Tile.P_White else Tile.P_White

    def evaluate(self, board, color, terminal_value=0):

        # Check if board state already exists in hash table
        board_repr = self.get_board_representation(board, color)
        if board_repr in self.hash_table:
            return self.hash_table[board_repr]

        """
        To improve the evaluate function, we can consider the following factors:

            1.Piece count: The more pieces a player has on the board, the better their position.
            2.Mobility: The more moves a player has available, the better their position.
            3.Connectivity: The more connected a player's pieces are to each other, the better their position.
            4.Corners: Controlling the corners of the board is advantageous.
            5.Center: Controlling the center of the board is advantageous.
        """

        """ Piece count factor """
        my_pieces = 0
        opponent_pieces = 0
        for row in board.game_board:
            for tile in row:
                if tile.piece == color:
                    my_pieces += 1
                elif tile.piece == self.opponent(color):
                    opponent_pieces += 1

        piece_count_factor = (my_pieces - opponent_pieces) * 10

        """ Mobility factor """
        valid_moves_color = self.generate_all_possible_moves(board, color)
        valid_moves_opponent = self.generate_all_possible_moves(board, self.opponent(color))

        mobility_factor = (len(valid_moves_color) - len(valid_moves_opponent)) * 10

        """ Connectivity factor """
        my_connected_groups = board.get_connected_groups(color)
        opponent_connected_groups = board.get_connected_groups(self.opponent(color))

        connectivity_factor = (len(my_connected_groups) - len(opponent_connected_groups)) * 10

        """ Corner factor """
        my_corners = 0
        opponent_corners = 0
        corner_positions = [(0, 0), (0, board.size - 1), (board.size - 1, 0), (board.size - 1, board.size - 1)]
        for pos in corner_positions:
            tile = board.game_board[pos[0]][pos[1]]
            if tile.piece == color:
                my_corners += 1
            elif tile.piece == self.opponent(color):
                opponent_corners += 1

        corner_factor = (my_corners - opponent_corners) * 100

        """ Center factor  """
        center_tile = board.game_board[board.size // 2][board.size // 2]
        my_center = 1 if center_tile.piece == color else 0
        opponent_center = 1 if center_tile.piece == self.opponent(color) else 0

        center_factor = (my_center - opponent_center) * 10

        value = piece_count_factor + mobility_factor + connectivity_factor + corner_factor + center_factor

        # Add board state and score to hash table
        self.hash_table[board_repr] = value

        return value

    def get_board_representation(self, board, color):
        # Generate a unique string representation of the board state
        pieces = ""
        for row in board.game_board:
            for tile in row:
                if tile.piece == Tile.P_Black:
                    pieces += "B"
                elif tile.piece == Tile.P_White:
                    pieces += "W"
                else:
                    pieces += "_"
        return pieces + str(color)
    """
     the KonaneGame class now has a hash_table attribute that is initialized as an empty dictionary 
     in the constructor. The evaluate method first checks if the board state already exists in the hash table 
     by generating its unique representation using the get_board_representation method. 
     If it does exist, the corresponding score is returned from the hash table.
     If it doesn't exist, the evaluation score is calculated and added to the hash table 
     with its corresponding board state representation as the key. 
     The get_board_representation method generates a string representation of the board state 
     by concatenating the symbols for each piece on the board (B for black, W for white, and _ for an empty tile)
     along with the current player's color. This ensures that identical board states with different players
     will have different representations and be treated separately in the hash table.
     """


