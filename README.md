# Terminal-Based 2048 Game

A command-line implementation of the popular 2048 puzzle game built with Python.

## Description

This is a terminal-based version of the classic 2048 game where you combine tiles with the same number to create a tile with the value 2048. The game is played on a 4x4 grid using keyboard controls.

## Features

- Clean terminal interface
- Real-time keyboard controls
- Game state display after each move
- In-game help menu
- Customizable controls via config.py

## Requirements

- Python 3.6+
- Required packages listed in `requirements.txt`

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/NERUZ-XOD/terminal_based_2048_game.git
   cd terminal_based_2048_game
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## How to Play

Run the game:
```
python 2048.py
```

### Controls
- **W**: Move tiles up
- **A**: Move tiles left
- **S**: Move tiles down
- **D**: Move tiles right
- **H**: Display help
- **Q**: Quit game

### Customizing Controls

You can customize the game controls and settings by editing the `config.py` file:

```python
# Controls
MOVE_UP = 'w'      # Change to customize the up movement key
MOVE_LEFT = 'a'    # Change to customize the left movement key
MOVE_DOWN = 's'    # Change to customize the down movement key
MOVE_RIGHT = 'd'   # Change to customize the right movement key
HELP = 'h'         # Change to customize the help key
QUIT = 'q'         # Change to customize the quit key

# Game Settings
INITIAL_TILES = 2  # Number of tiles to spawn at game start
TILE_SPAWN_DELAY = 0.2  # Delay after move before spawning new tile
MOVE_DELAY = 0.2   # Delay between moves to prevent multiple keypresses

# Display Settings
CLEAR_COMMAND = 'cls' if __name__ == 'nt' else 'clear'  # Command to clear terminal
CELL_WIDTH = 4     # Width of each cell in the display
```

### Rules
1. Tiles with the same number merge when they collide
2. After each move, a new tile (2 or 4) appears on the board
3. The game ends when the board is full and no more moves are possible
4. The goal is to create a tile with the value 2048

## License

This project is open source and available under the MIT License.

## Acknowledgements

Inspired by the original 2048 game created by Gabriele Cirulli.
