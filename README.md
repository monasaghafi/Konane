# Konane

## implement min and max functions (both separated) in Agent.py 
  being used as part of the minimax algorithm for determining the best move to make
  
## improve evaluate function cinsidering 5 factors:
"piece count factor"
calculates the number of pieces each player has on the board and assigns a score based on the difference between the numbers of pieces.

"mobility factor"
calculates the number of possible moves for each player, and assigns a score based on the difference between the numbers of valid moves. 

"connectivity factor"
determines the number of connected groups of pieces for each player on the board. If a player has more groups of connected pieces, they are assigned a higher score.

"corner factor"
awards points based on how many corner positions on the board are occupied by a player's pieces. The player with more pieces in the corners receives a higher score.

"center factor"
scores the player based on whether they control the center tile of the board.

All five of these factors are then combined into a single score, which is returned by the function.

## implementing hash table
 The evaluate method first checks if the board state already exists in the hash table by generating its unique representation using the get_board_representation method. If it does exist, the corresponding score is returned from the hash table. If it doesn't exist, the evaluation score is calculated and added to the hash table with its corresponding board state representation as the key. The get_board_representation method generates a string representation of the board state by concatenating the symbols for each piece on the board (B for black, W for white, and _ for an empty tile) along with the current player's color. This ensures that identical board states with different players will have different representations and be treated separately in the hash table.
