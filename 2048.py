import numpy as np
import random
import os
import keyboard
import time

class Game2048:
    def __init__(self):
        self.grid = np.zeros((4, 4), dtype=int)
        self.spawn_tile()
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
        if direction == 'w':  # Up
            self.grid = self.grid.T
            for i in range(4):
                self.grid[i] = self.compress(self.grid[i])
                self.grid[i] = self.merge(self.grid[i])
                self.grid[i] = self.compress(self.grid[i])
            self.grid = self.grid.T
        elif direction == 's':  # Down
            self.grid = self.grid.T
            for i in range(4):
                self.grid[i] = self.compress(self.grid[i][::-1])[::-1]
                self.grid[i] = self.merge(self.grid[i][::-1])[::-1]
                self.grid[i] = self.compress(self.grid[i][::-1])[::-1]
            self.grid = self.grid.T
        elif direction == 'a':  # Left
            for i in range(4):
                self.grid[i] = self.compress(self.grid[i])
                self.grid[i] = self.merge(self.grid[i])
                self.grid[i] = self.compress(self.grid[i])
        elif direction == 'd':  # Right
            for i in range(4):
                self.grid[i] = self.compress(self.grid[i][::-1])[::-1]
                self.grid[i] = self.merge(self.grid[i][::-1])[::-1]
                self.grid[i] = self.compress(self.grid[i][::-1])[::-1]
        # Spawn a new tile only if the grid has changed
        if not np.array_equal(original_grid, self.grid):
            self.spawn_tile()