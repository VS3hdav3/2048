import pygame
import random
import math
from tile import Tile
pygame.init()

width = 800
height = 800

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("2048")

clock = pygame.time.Clock()

rows = 4
cols = 4

# Size of tiles
rect_height = height // rows
rect_width = width // cols

outline_color = (156, 137, 120)
outline_thickness = 10
background_color = (189, 173, 152)
font_color_black = (117, 100, 82)
font_color_white = (255, 255, 255)

font = pygame.font.SysFont("ClearSans", 80, bold=True)
move_vel = 20

def drawGrid(window):
    for row in range(1, rows):
        y = row * rect_height
        pygame.draw.line(window, outline_color, (0, y), (width, y), outline_thickness)
    for col in range(1, cols):
        x = col * rect_width
        pygame.draw.line(window, outline_color, (x, 0), (x, height), outline_thickness)
    pygame.draw.rect(window, outline_color, (0, 0, width, height), outline_thickness)

def draw(window, tiles):
    window.fill(background_color)
    for tile in tiles.values():
        tile.draw(window, rect_width, rect_height, font, font_color_black, font_color_white)
    drawGrid(window)
    pygame.display.update()

def getRandomPos(tiles):
    row = None
    col = None
    while True:
        row = random.randrange(0, rows)
        col = random.randrange(0, cols)
        
        if f"{row}{col}" not in tiles:  # Using Dictionary allows for such checking, using the f string to pass whether the row or col is occupied or not
            break
    return row, col

def moveTiles(window, tiles, clock, direction):
    updated = True
    merged = set() # To not update already updated tiles, causing a chain-reaction. 1 merge per 2 tiles at a time
    
    if direction == "left":
        sort = lambda x: x.col
        reverse = False
        delta = (-move_vel, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")  # Gets left tile in the same row
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + move_vel
        move_check = (
            lambda tile, next_tile: tile.x > next_tile.x + rect_width + move_vel
        )
        ceil = True
    elif direction == "right":
        sort = lambda x: x.col
        reverse = True
        delta = (move_vel, 0)
        boundary_check = lambda tile: tile.col == cols - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - move_vel
        move_check = (
            lambda tile, next_tile: tile.x + rect_width + move_vel < next_tile.x
        )
        ceil = False
    elif direction == "up":
        sort = lambda x: x.row
        reverse = False
        delta = (0, -move_vel)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + move_vel
        move_check = (
            lambda tile, next_tile: tile.y > next_tile.y + rect_height + move_vel
        )
        ceil = True
    elif direction == "down":
        sort = lambda x: x.row
        reverse = True
        delta = (0, move_vel)
        boundary_check = lambda tile: tile.row == rows - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - move_vel
        move_check = (
            lambda tile, next_tile: tile.y + rect_height + move_vel < next_tile.y
        )
        ceil = False
    
    while updated:
        clock.tick(60)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort, reverse=reverse)
        
        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue
            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif (tile.val == next_tile.val 
                  and tile not in merged 
                  and next_tile not in merged):
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    next_tile.val *= 2
                    sorted_tiles.pop(i)
                    merged.add(next_tile)
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue
            tile.setPos(rect_width, rect_height, ceil)
            updated = True
        
        updateTiles(window, tiles, sorted_tiles)
    return endMove(tiles)

def endMove(tiles):
    # Check if the grid is full
    if len(tiles) == 16:
        # Check for any possible moves
        for tile in tiles.values():
            # Check neighbors for possible merges
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor_key = f"{tile.row + dr}{tile.col + dc}"
                neighbor = tiles.get(neighbor_key)
                if neighbor and neighbor.val == tile.val:
                    return "continue"  # Still possible to merge tiles
        return "lost"  # No moves left
    
    # If grid isn't full, add a new tile
    row, col = getRandomPos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col, rect_width, rect_height)
    return "continue"

def showPopup(window):
    popup_width = 400
    popup_height = 200
    popup_x = (width - popup_width) // 2
    popup_y = (height - popup_height) // 2
    button_width = 150
    button_height = 50
    button_margin = 20
    button_font = pygame.font.SysFont("ClearSans", 25, bold=True)
    
    new_game_button = pygame.Rect(popup_x + button_margin, popup_y + popup_height - button_height - button_margin, button_width, button_height)
    exit_button = pygame.Rect(popup_x + popup_width - button_width - button_margin, popup_y + popup_height - button_height - button_margin, button_width, button_height)
    
    popup_width = 600
    popup_height = 400
    popup_x = (width - popup_width) // 2
    popup_y = (height - popup_height) // 2
    
    pygame.draw.rect(window, background_color, (popup_x, popup_y, popup_width, popup_height))
    pygame.draw.rect(window, outline_color, (popup_x, popup_y, popup_width, popup_height), outline_thickness)
    
    message = font.render("You Lost!", True, font_color_black)
    window.blit(message, (popup_x + (popup_width - message.get_width()) // 2, popup_y + 50))
    
    button_width = 160
    button_height = 60
    button_margin = 70
    
    new_game_button = pygame.Rect(popup_x + button_margin, popup_y + popup_height - 150, button_width, button_height)
    exit_button = pygame.Rect(popup_x + popup_width - button_width - button_margin, popup_y + popup_height - 150, button_width, button_height)
    
    pygame.draw.rect(window, outline_color, new_game_button)
    pygame.draw.rect(window, outline_color, exit_button)
    
    new_game_text = button_font.render("New Game", True, font_color_white)
    exit_text = button_font.render("Exit", True, font_color_white)
    window.blit(new_game_text, (new_game_button.x + (button_width - new_game_text.get_width()) // 2, new_game_button.y + 10))
    window.blit(exit_text, (exit_button.x + (button_width - exit_text.get_width()) // 2, exit_button.y + 10))
    
    pygame.display.update()
    
    # Handle button interactions
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.collidepoint(event.pos):
                    return "new_game"
                elif exit_button.collidepoint(event.pos):
                    return "quit"


def updateTiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile
    
    draw(window, tiles)

def generateTiles():
    tiles = {}
    for _ in range(2):
        row, col = getRandomPos(tiles)
        tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col, rect_width, rect_height)
    return tiles

def main():
    run = True
    tiles = generateTiles()
    result = "continue"
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    result = moveTiles(win, tiles, clock, "left")
                if event.key == pygame.K_RIGHT:
                    result = moveTiles(win, tiles, clock, "right")
                if event.key == pygame.K_UP:
                    result = moveTiles(win, tiles, clock, "up")
                if event.key == pygame.K_DOWN:
                    result = moveTiles(win, tiles, clock, "down")
        if result == "lost":
            action = showPopup(win)
            if action == "new_game":
                tiles = generateTiles()
                result = "continue"
            else:
                run = False
        draw(win, tiles)
    pygame.quit()
    quit()   

if __name__ == "__main__":
    main()