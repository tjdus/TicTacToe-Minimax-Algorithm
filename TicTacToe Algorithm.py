import pygame
import random

WIDTH = 600
HEIGHT = 700

length = 150

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
font= pygame.font.SysFont(font_name, 150, False, False)
tfont = pygame.font.SysFont(font_name, 150, False, False)
afont = pygame.font.SysFont(font_name, 50, False, False)

def DrawBoard(board):
    for i in range(2):
        for j in range(3):
            pygame.draw.line(screen, BLACK, [75+j*length, 150+ (i+1)*length], [75+(j+1)*length, 150 + (i+1)*length], 4)
            pygame.draw.line(screen, BLACK, [75+(i+1)*length, 150+ j*length], [75+(i+1)*length, 150 + (j+1)*length], 4)
    for i in range(3):
        for j in range(3):
            b= font.render(board[i*3+j], True, BLACK)
            screen.blit(b, [110+j*length, 180+i*length])

def playagainscreen(winner):
    screen.fill(WHITE)
    text = afont.render("Do you want to play again?", True, BLACK)
    screen.blit(text, [50, 200])
    text = tfont.render("Yes or No", True, BLACK)
    screen.blit(text, [50, 300])
    if winner=='player':
        text = tfont.render("You Win!", True, RED)
        screen.blit(text, [50, 50])
    elif winner=='computer':
        text = tfont.render("You Lose!", True, RED)
        screen.blit(text, [50, 50])
    else:
        text = tfont.render("Tie!", True, RED)
        screen.blit(text, [200, 50])
def makeMove(board, letter, move):
    board[move] = letter

def IsEmpty(board, move):
    return board[move]== ' '

def GetBoardCopy(board):
    boardCopy=[]
    for i in board:
        boardCopy.append(i)
    return boardCopy

def Result(board, letter):
    if (board[6] == board[7] and board[7]==board[8] and board[8] == letter) or \
    (board[0] == board[1] and board[1]==board[2] and board[2] == letter) or \
    (board[3] == board[4] and board[4]==board[5] and board[5] == letter) or \
    (board[6] == board[3] and board[3]==board[0] and board[0] == letter) or \
    (board[7] == board[4] and board[4]==board[1] and board[1] == letter) or \
    (board[8] == board[5] and board[2]==board[5] and board[5] == letter) or \
    (board[6] == board[4] and board[4]==board[2] and board[2] == letter) or \
    (board[8] == board[4] and board[4]==board[0] and board[0] == letter) or \
    (board[6] == board[7] and board[7]==board[8] and board[8] == letter) :
        if letter == player:
            return 'player'
        elif letter == computer:
            return 'computer'
    return None

def Minimax(board, turn):
    if turn == 'computer':
        next = 'player'
    else:
        next= 'computer'
        
    if Result(board, computer) == 'computer':
        return 1
    elif Result(board, computer) == 'player':
        return -1
    elif IsBoardFull(board):
        return 0
    
    if turn=='computer':
        bestscore = float('-inf')
        for i in range(9):
            if IsEmpty(board, i):
                boardCopy = GetBoardCopy(board)
                makeMove(boardCopy, computer, i)
                score = Minimax(boardCopy, next)
                bestscore = max(score, bestscore)
    else:
        bestscore = float('inf')
        for i in range(9):
            if IsEmpty(board, i):
                boardCopy = GetBoardCopy(board)
                makeMove(boardCopy, player, i)
                score = Minimax(boardCopy, next)
                bestscore = min(score, bestscore) 
    return bestscore            
                
def GetComputerMove(board, computer):
    for i in range(9):
        boardCopy = GetBoardCopy(board)
        if IsEmpty(boardCopy, i):
            makeMove(boardCopy,computer, i)
            if Result(boardCopy, computer):
                return i
    
    for i in range(9):
        boardCopy=GetBoardCopy(board)
        if IsEmpty(boardCopy, i):
            makeMove(boardCopy, player, i)
            if Result(boardCopy, player):
                return i
    position= -1
    bestscore = float('-inf')
    for i in range(9):
        if IsEmpty(board, i):
            boardCopy = GetBoardCopy(board)
            makeMove(boardCopy, computer, i)
            score = Minimax(boardCopy, 'computer')
            if bestscore < score:
                bestscore = score
                position = i
                
    return position


    
def IsBoardFull(board):
    for i in range(9):
        if IsEmpty(board, i):
            return False
    return True


done = False

board=[' '] * 9
getinput = False

move=-1
player = 'O'
computer = 'X'
winner=None   
turn = 'player'
gameIsplaying =True
playagain = False
screen.fill(WHITE)

while not done: 
    if not playagain:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y= pygame.mouse.get_pos()
                if x>=75 and x<=525 and y>=150 and y<=600:
                    if x<225:
                        if y<300:
                            move=0
                        elif y<450:
                            move=3
                        else:
                            move=6
                    elif x<375:
                        if y<300:
                            move=1
                        elif y<450:
                            move=4
                        else:
                            move=7
                    else:
                        if y<300:
                            move=2
                        elif y<450:
                            move=5
                        else:
                            move=8
                else:
                    move= -1      
        if move!=-1:
            if IsEmpty(board, move):
                getinput=True
            else:
                move=-1 
        
        while gameIsplaying:
            if turn == 'player' and getinput:
                makeMove(board, player, move) 
                getinput=False   
                if Result(board, player)=='player':
                    gameIsplaying = False
                    playagain=True   
                    winner = 'player'               
                else:
                    if IsBoardFull(board):
                        winner = None
                        gameIsplaying=False
                        playagain=True
                        break
                    else:
                        turn = 'computer' 
            elif turn == 'computer':
                move= GetComputerMove(board, computer)
                makeMove(board, computer, move)
                move=-1
                if Result(board, computer)=='computer':
                    winner ='computer'                    
                    gameIsplaying=False
                    playagain=True
                else:
                    if IsBoardFull(board):
                        winner = None
                        gameIsplaying=False
                        playagain=True
                        break
                    else:
                        turn = 'player'
            else:
                break
        screen.fill(WHITE)
        DrawBoard(board)    
    else:
        playagainscreen(winner)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y= pygame.mouse.get_pos()
                if x<300:
                    playagain=True
                    board=[' ']*9
                    getinput = False
                    move=-1
                    player = 'O'
                    computer = 'X'
                    winner=None    
                    turn = 'player'
                    gameIsplaying =True
                    playagain = False
                    
                else:
                    done=True
    # ????????? ?????? ?????????
    
    # ????????? ????????? ??????

    # ?????? ????????????
    pygame.display.flip()

    # ?????? 60 ??????????????? ????????????
    clock.tick(60)

# ?????? ??????
pygame.quit()
