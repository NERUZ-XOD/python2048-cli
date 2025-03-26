import os

# Game Configuration Settings

# Controls
MOVE_UP = 'w'      # Key to move tiles up
MOVE_LEFT = 'a'    # Key to move tiles left
MOVE_DOWN = 's'    # Key to move tiles down
MOVE_RIGHT = 'd'   # Key to move tiles right
HELP = 'h'         # Key to display help
QUIT = 'q'         # Key to quit the game

# Game Settings
INITIAL_TILES = 2  # Number of tiles to spawn at game start
TILE_SPAWN_DELAY = 0.2  # Delay after move before spawning new tile
MOVE_DELAY = 0.2   # Delay between moves to prevent multiple keypresses

# Display Settings
CLEAR_COMMAND = 'cls' if os.name == 'nt' else 'clear'  # Command to clear terminal
CELL_WIDTH = 4     # Width of each cell in the display
