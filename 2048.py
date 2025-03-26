import numpy as np
import random
import os
import time
import config  # Import the config module
import sys

# Try to import keyboard module, fall back to platform-specific alternatives if not available
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    # Try to import msvcrt for Windows as a fallback
    if os.name == 'nt':
        import msvcrt
    else:
        # For Unix systems, we'll use a different approach
        try:
            import termios
            import tty
            import select
            UNIX_SPECIAL_CHARS = True
        except ImportError:
            UNIX_SPECIAL_CHARS = False

class Game2048:
    def __init__(self):
        self.grid = np.zeros((4, 4), dtype=int)
        self.score = 0
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
                self.score += row[i]  # Add to score when tiles merge
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
        
        # Return whether the grid has changed
        grid_changed = not np.array_equal(original_grid, self.grid)
        
        # Spawn a new tile only if the grid has changed
        if grid_changed:
            self.spawn_tile()
            
        return grid_changed
            
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
        print(f"Score: {self.score}")
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
        print(f"  {config.HELP.upper()} - Help")
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

def get_key_windows():
    """Get a single keypress from the user (Windows-specific)"""
    if msvcrt.kbhit():
        key = msvcrt.getch().decode('utf-8', errors='ignore').lower()
        return key
    return None

def get_key_unix():
    """Get a single keypress from the user (Unix-specific)"""
    if UNIX_SPECIAL_CHARS:
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            old_settings = termios.tcgetattr(sys.stdin)
            try:
                tty.setcbreak(sys.stdin.fileno())
                key = sys.stdin.read(1)
                return key.lower()
            finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    return None

def get_key():
    """Cross-platform function to get a keypress without waiting for Enter"""
    if KEYBOARD_AVAILABLE:
        # Use the keyboard module if available
        for key in [config.MOVE_UP, config.MOVE_DOWN, config.MOVE_LEFT, config.MOVE_RIGHT, 
                   config.HELP, config.QUIT]:
            if keyboard.is_pressed(key):
                return key
        return None
    elif os.name == 'nt':
        # Windows fallback
        return get_key_windows()
    else:
        # Unix fallback
        return get_key_unix()

def main():
    game = Game2048()
    print("Loading game...")
    time.sleep(1)  # Brief pause to ensure keyboard detection is ready
    
    # Show initial game state
    game.display()
    
    if not KEYBOARD_AVAILABLE and not (os.name == 'nt' or UNIX_SPECIAL_CHARS):
        print("Warning: Real-time keyboard input not available.")
        print("You'll need to press Enter after each key.")
        print("Use standard input mode instead.")
        # Fall back to standard input mode if no real-time input method is available
        while True:
            if game.is_game_over():
                game.display()
                print("Game Over! No more moves left.")
                break
                
            print("Enter your move: ", end="", flush=True)
            key = input().lower()
            
            if key:
                if key in [config.MOVE_UP, config.MOVE_DOWN, config.MOVE_LEFT, config.MOVE_RIGHT]:
                    grid_changed = game.move(key)
                    if grid_changed:
                        game.display()
                elif key == config.HELP:
                    display_help()
                    game.display()
                elif key == config.QUIT:
                    print("Thanks for playing!")
                    break
    else:
        # Use real-time keyboard input
        last_key_pressed = None
        
        while True:
            if game.is_game_over():
                game.display()
                print("Game Over! No more moves left.")
                break
            
            # Get keyboard input
            key = get_key()
            
            if key:
                if key in [config.MOVE_UP, config.MOVE_DOWN, config.MOVE_LEFT, config.MOVE_RIGHT]:
                    if key != last_key_pressed:  # Only process if it's a new key
                        grid_changed = game.move(key)
                        if grid_changed:
                            game.display()
                        last_key_pressed = key
                elif key == config.HELP:
                    display_help()
                    game.display()
                    last_key_pressed = None
                elif key == config.QUIT:
                    print("Thanks for playing!")
                    break
            else:
                last_key_pressed = None  # Reset when no key is pressed
            
            # Small delay to prevent CPU overuse
            time.sleep(0.05)

if __name__ == "__main__":
    main()