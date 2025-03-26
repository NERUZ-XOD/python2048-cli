import numpy as np
import random
import os
import keyboard
import time
import config  # Import the config module

class Game2048:
    def __init__(self):
        self.grid = np.zeros((4, 4), dtype=int)
        # Use config for initial tiles
        for _ in range(config.INITIAL_TILES):
            self.spawn_tile()
    
    def spawn_tile(self):
        empty_cells = [(r, c) for r in range(4) for c in range(4) if self.grid[r, c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r, c] = 2 if random.random() < 0.9 else 4
    
    def compress(self, row):
        new_row = [num for num in row if num != 0]  # Remove zeros
        new_row += [0] * (4 - len(new_row))  # Fill remaining spaces with zeros
        return new_row
    
    def merge(self, row):
        for i in range(3):
            if row[i] == row[i+1] and row[i] != 0:
                row[i] *= 2
                row[i+1] = 0
        return row
    
    def move(self, direction):
        original_grid = self.grid.copy()  # Save the original grid to check for changes
        if direction == config.MOVE_UP:  # Up
            self.grid = self.grid.T
            for i in range(4):
                self.grid[i] = self.compress(self.grid[i])
                self.grid[i] = self.merge(self.grid[i])
                self.grid[i] = self.compress(self.grid[i])
            self.grid = self.grid.T
        elif direction == config.MOVE_DOWN:  # Down
            self.grid = self.grid.T
            for i in range(4):
                self.grid[i] = self.compress(self.grid[i][::-1])[::-1]
                self.grid[i] = self.merge(self.grid[i][::-1])[::-1]
                self.grid[i] = self.compress(self.grid[i][::-1])[::-1]
            self.grid = self.grid.T
        elif direction == config.MOVE_LEFT:  # Left
            for i in range(4):
                self.grid[i] = self.compress(self.grid[i])
                self.grid[i] = self.merge(self.grid[i])
                self.grid[i] = self.compress(self.grid[i])
        elif direction == config.MOVE_RIGHT:  # Right
            for i in range(4):
                self.grid[i] = self.compress(self.grid[i][::-1])[::-1]
                self.grid[i] = self.merge(self.grid[i][::-1])[::-1]
                self.grid[i] = self.compress(self.grid[i][::-1])[::-1]
        # Spawn a new tile only if the grid has changed
        if not np.array_equal(original_grid, self.grid):
            self.spawn_tile()
            
    def is_game_over(self):
        if 0 in self.grid:
            return False
        for i in range(4):
            for j in range(3):
                if self.grid[i, j] == self.grid[i, j+1] or self.grid[j, i] == self.grid[j+1, i]:
                    return False
        return True
    
    def display(self):
        os.system(config.CLEAR_COMMAND)
        print("2048 Game")
        print(f"Use {config.MOVE_UP}/{config.MOVE_LEFT}/{config.MOVE_DOWN}/{config.MOVE_RIGHT} to move. Press {config.QUIT} to quit. Press {config.HELP} for help.")
        print("---------------------")
        for row in self.grid:
            print('|'.join(f"{num:^{config.CELL_WIDTH}}" if num != 0 else " " * config.CELL_WIDTH for num in row))
            print("---------------------")

def display_help():
    try:
        os.system(config.CLEAR_COMMAND)  # Clear screen before showing help
        print("\n=== 2048 GAME HELP ===\n")
        print("OBJECTIVE: Combine tiles to reach 2048")
        print("\nCONTROLS:")
        print(f"  {config.MOVE_UP.upper()} - Move Up")
        print(f"  {config.MOVE_LEFT.upper()} - Move Left")
        print(f"  {config.MOVE_DOWN.upper()} - Move Down")
        print(f"  {config.MOVE_RIGHT.upper()} - Move Right")
        print(f"  {config.QUIT.upper()} - Quit Game")
        print("\nGAMEPLAY:")
        print("- Tiles with the same number merge when they collide")
        print("- A new 2 or 4 tile appears after each move")
        print("- Game ends when the board is full and no moves are possible")
        print("\nPress Enter to return to the game...")
        input()
    except Exception as e:
        print(f"Error displaying help: {e}")
        print("Press Enter to continue...")
        input()

def main():
    game = Game2048()
    print("Loading game...")
    time.sleep(1)  # Brief pause to ensure keyboard detection is ready
    
    # Show initial game state
    game.display()
    print(f"Use {config.MOVE_UP}/{config.MOVE_LEFT}/{config.MOVE_DOWN}/{config.MOVE_RIGHT} to move, {config.HELP} for help, {config.QUIT} to quit")
    
    while True:
        if game.is_game_over():
            game.display()
            print("Game Over! No more moves left.")
            break
        
        # Real-time key detection
        try:
            if keyboard.is_pressed(config.MOVE_UP):
                game.move(config.MOVE_UP)
                game.display()
                time.sleep(config.MOVE_DELAY)  # Brief delay to avoid multiple moves per keypress
            elif keyboard.is_pressed(config.MOVE_LEFT):
                game.move(config.MOVE_LEFT)
                game.display()
                time.sleep(config.MOVE_DELAY)
            elif keyboard.is_pressed(config.MOVE_DOWN):
                game.move(config.MOVE_DOWN)
                game.display()
                time.sleep(config.MOVE_DELAY)
            elif keyboard.is_pressed(config.MOVE_RIGHT):
                game.move(config.MOVE_RIGHT)
                game.display()
                time.sleep(config.MOVE_DELAY)
            elif keyboard.is_pressed(config.HELP):
                display_help()
                game.display()
            elif keyboard.is_pressed(config.QUIT):
                print("Thanks for playing!")
                break
        except Exception as e:
            print(f"Error: {e}")
            print("Press Enter to continue...")
            input()
            game.display()

if __name__ == "__main__":
    main()