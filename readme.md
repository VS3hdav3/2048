# 2048 Game

This project implements the popular 2048 game using Python and Pygame. The game consists of sliding and merging numbered tiles to reach the highest possible value of 2048. This project aims to demonstrate the use of object-oriented programming to create the game mechanics and graphical interface.

## **Overview**

The 2048 game involves a 4x4 grid where players use arrow keys to slide tiles. When two tiles with the same number collide, they merge into one, and their value doubles. The game continues until no more moves are possible or a tile with the value 2048 is created.

## **Components**

### **1. Main Script (`main.py`)**
The `main.py` script contains the game loop and handles the interactions between the game elements:
- **Game Initialization:** Configures the game window size, colors, fonts, and the initial game state.
- **Game Loop:** 
  - Handles player inputs (arrow keys) to move the tiles.
  - Manages the merging logic, ensuring tiles combine when appropriate.
  - Updates the tiles’ positions on the grid and checks for game over conditions.
- **Helper Functions:** Functions like `getRandomPos()` and `moveTiles()` are used to handle tile generation and movement mechanics.
  
### **2. Tile Class (`tile.py`)**
The `Tile` class manages the individual tiles within the grid:
- **Attributes:**
  - `val`: The value of the tile (e.g., 2, 4, 8, etc.).
  - `row` and `col`: The row and column positions of the tile in the grid.
  - `x` and `y`: The pixel coordinates for rendering the tile on the screen.
- **Methods:**
  - `getColor()`: Returns the color of the tile based on its value.
  - `draw()`: Renders the tile on the game window.
  - `move()`: Updates the tile's position based on the movement delta.
  - `setPos()`: Adjusts the tile’s position based on grid boundaries after movement.

### **3. Game Mechanics**
- **Tile Movement:** Tiles are moved by using arrow keys (up, down, left, right). Each move slides the tiles in the specified direction, and adjacent tiles with the same value merge into one.
- **Merge Logic:** When two tiles with the same value collide, they combine to form a tile with double the value. Each merge is restricted to one per pair of tiles.
- **Game Over:** The game ends when no more valid moves are possible. The player can also start a new game or quit after losing.
- **Tile Generation:** A new tile (either 2 or 4) is randomly placed on the grid after each move.

## **Gameplay Instructions**
1. **Start the Game**: Run the script `main.py` to launch the game window.
2. **Move Tiles**: Use the arrow keys to move the tiles:
   - **Left**: Move all tiles left, merging when possible.
   - **Right**: Move all tiles right, merging when possible.
   - **Up**: Move all tiles up, merging when possible.
   - **Down**: Move all tiles down, merging when possible.
3. **Merge Tiles**: When two tiles with the same number collide, they merge into one, and their value doubles.
4. **Game Over**: The game ends when there are no more possible moves. You can restart the game or quit after losing.

## **File Breakdown**

### **1. `main.py`**
- Main game loop that controls the game flow, handles player input, and updates the screen.
- The function `moveTiles()` updates the tiles and merges them based on the user’s movement input.
- The function `showPopup()` is used to display the game-over message and options to start a new game or quit.

### **2. `tile.py`**
- Defines the `Tile` class, which is responsible for the creation, movement, and drawing of each tile.
- The tile’s color changes dynamically based on its value using a pre-defined color list.
