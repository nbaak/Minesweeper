import pygame
import random
import datetime
import settings

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set the dimensions of the window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

# Set the dimensions of the grid
GRID_SIZE = settings.GRID_SIZE
CELL_SIZE = WINDOW_WIDTH // GRID_SIZE

# Set the number of mines
NUM_MINES = settings.NUM_MINES

# Set the font for text rendering
FONT_SIZE = 20
FONT = pygame.font.Font(None, FONT_SIZE)

# Create the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Minesweeper")

# Function to create the game board
def create_board():
    board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    mines = []
    
    while len(mines) < NUM_MINES:
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)
        
        if (row, col) not in mines:
            mines.append((row, col))
            board[row][col] = -1
            
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if 0 <= i < GRID_SIZE and 0 <= j < GRID_SIZE and board[i][j] != -1:
                        board[i][j] += 1
    
    return board

# Function to reveal a cell
def reveal_cell(row, col):
    if revealed[row][col]:
        return
    
    revealed[row][col] = True
    
    if board[row][col] == -1:
        game_over()
    elif board[row][col] == 0:
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i < GRID_SIZE and 0 <= j < GRID_SIZE:
                    reveal_cell(i, j)

# Function to mark a cell as a mine
def mark_cell(row, col):
    if not revealed[row][col]:
        marked[row][col] = not marked[row][col]

# Function to handle game over
def game_over():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            revealed[row][col] = True

# Function to reset the game
def reset_game():
    global board, revealed, marked
    board = create_board()
    revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
    marked = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]

# Function to draw the grid
def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            
            if revealed[row][col]:
                pygame.draw.rect(window, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
                
                if board[row][col] == -1:
                    pygame.draw.circle(window, RED, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 4)
                elif board[row][col] > 0:
                    text = FONT.render(str(board[row][col]), True, BLACK)
                    text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                    window.blit(text, text_rect)
            else:
                if marked[row][col]:
                    pygame.draw.rect(window, GRAY, (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.circle(window, RED, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 4)
                else:
                    pygame.draw.rect(window, GRAY, (x, y, CELL_SIZE, CELL_SIZE))
    
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(window, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_HEIGHT))
        pygame.draw.line(window, BLACK, (0, i * CELL_SIZE), (WINDOW_WIDTH, i * CELL_SIZE))

# Function to take a screenshot
def take_screenshot():
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    pygame.image.save(window, filename)
    print(f"Screenshot saved as {filename}")

# Create the game board
board = create_board()
revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
marked = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            col = pos[0] // CELL_SIZE
            row = pos[1] // CELL_SIZE
            
            if event.button == 1:
                reveal_cell(row, col)
            elif event.button == 3:
                mark_cell(row, col)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
            elif event.key == pygame.K_s:
                take_screenshot()
    
    # Clear the window
    window.fill(BLACK)
    
    # Draw the grid
    draw_grid()
    
    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
