import pygame, sys
import numpy
import math

# Initialize pygame and create solid background
pygame.init()

# Constant Values
WIDTH = 600
HEIGHT = WIDTH
SIZE = WIDTH, HEIGHT
BACKGROUND = 25, 25, 25
LINE = 55, 55, 55
X_COLOR = 255, 0, 0
CIRCLE_COLOR = 0, 0, 255
ROWS = 3
COLUMNS = 3

# Create background display
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("TIC TAC TOE")
screen.fill(BACKGROUND)

# board model
board = numpy.zeros( (3, 3) )

def draw_board():

    # Draw splitting-lines
    pygame.draw.line(screen, LINE, (0, HEIGHT / 3), (WIDTH, HEIGHT / 3), 10)
    pygame.draw.line(screen, LINE, (0, (2 * HEIGHT) / 3), (WIDTH, (2 * HEIGHT) / 3), 10)
    pygame.draw.line(screen, LINE, (WIDTH / 3, 0), (WIDTH / 3, HEIGHT), 10)
    pygame.draw.line(screen, LINE, ((2 * WIDTH) / 3, 0), ((2 * WIDTH) / 3, HEIGHT), 10)

    # Draw thin border
    pygame.draw.line(screen, LINE, (0, 0), (WIDTH , 0), 3)
    pygame.draw.line(screen, LINE, (0, 0), (0, HEIGHT), 3)
    pygame.draw.line(screen, LINE, (WIDTH , 0), (WIDTH , HEIGHT), 3)
    pygame.draw.line(screen, LINE, (0, HEIGHT), (WIDTH , HEIGHT), 3)

    # Draw design
    pygame.draw.line(screen, BACKGROUND, (0, WIDTH / 3), (WIDTH , (HEIGHT / 3)), 3)
    pygame.draw.line(screen, BACKGROUND, (0, (2 * WIDTH / 3)), (WIDTH , (2 * HEIGHT / 3)), 3)
    pygame.draw.line(screen, BACKGROUND, (WIDTH / 3, 0), (WIDTH / 3, HEIGHT), 3)
    pygame.draw.line(screen, BACKGROUND, ((2 * WIDTH / 3), 0), ((2 * HEIGHT / 3), HEIGHT), 3)

# Draw characters depending on which player made the move
def draw_move():
    # iterate through entire board and draw the figures centered in every square
    for i in range(ROWS):
        for j in range(COLUMNS):
            # player 1 = Circle
            if board[i][j] == 1:                    #x                       y
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(j * WIDTH / 3 + WIDTH / 6), int(i * (HEIGHT / 3) + WIDTH / 6)), WIDTH * (3 / 20), 15)
            # player 2 = X
            elif board[i][j] == 2:
                pygame.draw.line(screen, X_COLOR, (int(j * WIDTH / 3 + 15), int(i * (HEIGHT / 3) + 15)), (int(j * WIDTH / 3 + WIDTH / 3 - 15), int(i * (HEIGHT / 3) + WIDTH / 3 - 15)), 15)
                pygame.draw.line(screen, X_COLOR, (int(j * WIDTH / 3 + WIDTH / 3 - 15), int(i * (HEIGHT / 3) + 15)), (int(j * WIDTH / 3 + 15), int(i * (HEIGHT / 3) + WIDTH / 3 - 15)), 15)

# update the board 2d list to make move in backend
def make_move(row, col, player):
    board[row][col] = player

# check whether a given position is empty
def available(currentBoard, row, col):
    if currentBoard[row][col] == 0:
        return True
    return False

# check whether the entire board is full 
def board_full(currentBoard):
    for i in range(3):
        for j in range(3):
            if currentBoard[i][j] == 0:
                return False
    return True 

# check whether a player has won the game (VISUAL)
def check_winner(player):
    # vertical winner
    for i in range(3):
        if board[0][i] == player and board[1][i] == player and board[2][i] == player:
            draw_vert_dash(i, player)
            return True
    
    # horizontal winner
    for i in range(3):
        if board[i][0] == player and board[i][1] == player and board[i][2] == player:
            draw_hori_dash(i, player)
            return True
    
    # desc diagonal winner
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_dash(player) 
        return True

    # asc diagonal winner
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_dash(player)
        return True
    
    return False

# Check if player has won game (NOT FINAL - NO VISUAL)
def check_winner_temp(player):
    # vertical winner
    for i in range(3):
        if board[0][i] == player and board[1][i] == player and board[2][i] == player:
            return True
    
    # horizontal winner
    for i in range(3):
        if board[i][0] == player and board[i][1] == player and board[i][2] == player:
            return True
    
    # desc diagonal winner
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        return True

    # asc diagonal winner
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    
    return False

# draw vertical strikethrough if a player has won
def draw_vert_dash(col, player):
    # draw a line through the winnning chain
    posX = col * WIDTH / 3 + WIDTH / 6
    
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = X_COLOR

    pygame.draw.line(screen, color, (posX, 10), (posX, WIDTH - 10), 15)

# draw horizontal strikethrough if a player has won
def draw_hori_dash(row, player):
    posY = row * (HEIGHT / 3) + WIDTH / 6

    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = X_COLOR

    pygame.draw.line(screen, color, (5, posY), (WIDTH - 5, posY), 15)

# draw an ascending strikethrough if a player has won
def draw_asc_dash(player):
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = X_COLOR

    pygame.draw.line(screen, color, (5, WIDTH - 5), (WIDTH - 5, 5), 15)

# draw a descending strikethrough if a player has won
def draw_desc_dash(player):
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = X_COLOR

    pygame.draw.line(screen, color, (5, 5), (WIDTH - 5, WIDTH - 5), 15)

# reset values to prepare for a new game
def restart():
    screen.fill(BACKGROUND)
    draw_board()
    for i in range(3):
        for j in range(3):
            board[i][j] = 0
    player = 2

def computerMove():   
    # current player = computer, next player = human 
    global player
    nextPlayer = player % 2 + 1

    # initialize value so low so that first available space will replace this val
    bestScore = -1 * math.inf
    bestPosition = [-100, -100]
    bestDepth = math.inf

    # check every position on the grid
    for i in range(3):
        for j in range(3):
            if available(board, i, j):
                # temporarily place the AI in the space and see what happens
                board[i][j] = player
                bestMove = minimax(0, False)
                # Reset that board position to make sure we only make the best move
                board[i][j] = 0
                if bestMove[0] > bestScore or (bestMove[0] == bestScore and bestDepth > bestMove[1]):
                    bestScore = bestMove[0]
                    bestPosition = [i, j]
    
    board[bestPosition[0]][bestPosition[1]] = player


def minimax(depth, maximizing):
    global player
    nextPlayer = player % 2 + 1
    # if AI won, return 1
    if check_winner_temp(player):
        return [1, depth]
    # if other player won, return -1
    if check_winner_temp(nextPlayer):
        return [-1, depth]
    # in case of a tie, return 0
    if (board_full(board) == True):
        return [0, depth]

    if maximizing:
        bestScore = -1 * math.inf
        bestDepth = math.inf

        for i in range(3):
            for j in range(3):
                if available(board, i, j):
                    board[i][j] = player
                    bestMove = minimax(depth + 1, False)
                    board[i][j] = 0
                    if bestMove[0] > bestScore or (bestMove[0] == bestScore and bestMove[1] < bestDepth):
                        bestScore = bestMove[0]
                        bestDepth = bestMove[1]
        return [bestScore, bestDepth]
    else:
        bestScore = math.inf
        bestDepth = math.inf

        for i in range(3):
            for j in range(3):
                if available(board, i, j):
                        board[i][j] = nextPlayer
                        bestMove = minimax(depth + 1, True)
                        board[i][j] = 0
                        if bestMove[0] < bestScore or (bestMove[0] == bestScore and bestDepth > bestMove[1]):
                            bestScore = bestMove[0]
                            bestDepth = bestMove[1]
        return [bestScore, bestDepth]


# initialize with the X player going first and with the game not being over
player = 2
game_over = False

# main loop
draw_board()
while True:
    for event in pygame.event.get():
        # if user exits the app, close the program
        if event.type == pygame.QUIT:
            sys.exit()
        
        # if user clicks mouse within app and game is active
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player == 1:
            # get mouse click location
            mouseX = event.pos[0] 
            mouseY = event.pos[1] 
            
            # determine position in 2d list we need to modify
            clicked_row = int(mouseY // (WIDTH / 3))
            clicked_column = int(mouseX // (HEIGHT / 3))

            # check whether the square that the user clicked is available, if so make a move and check for a winner
            if available(board, clicked_row, clicked_column):
                make_move(clicked_row, clicked_column, player)
                if check_winner(player):
                    game_over = True
                # after a move has been made, alternate to the other player
                player = player % 2 + 1

                # redraw the board after the move has been made in the backend
                draw_move()
        
        if game_over == False and player == 2 and board_full(board) == False:
            if (board[1][1] == 0):
                board[1][1] = 2
            else:
                computerMove()
            if check_winner(player):
                    game_over = True
            # after a move has been made, alternate to the other player
            player = player % 2 + 1

            # redraw the board after the move has been made in the backend
            draw_move()

        # if board is full and nobody won, then it must be a tie      
        if board_full(board):
            game_over = True
            player = 2
        
        # if the game is over, the user can press the spacebar to restart
        if event.type == pygame.KEYDOWN and game_over == True:
            if event.key == pygame.K_SPACE:
                restart()
                game_over = False
        

    
    pygame.display.update()

