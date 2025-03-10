import random
from time import sleep



test_board = """
_1_|_2_|_3_
_4_|_5_|_6_
 7 | 8 | 9
"""

board_dia = {1:2,2:6,3:10,4:14,5:18,6:22,7:26,8:30,9:34}

winning_combo = ({1,2,3},{4,5,6},{7,8,9},{1,4,7},{2,5,8},{3,6,9},{1,5,9},{3,5,7})

def game_play(player,board_pointer,board,player_pointers,player_tracking):
    '''
    logic to loop the player till they correctly input the number and return if they won or draw
    '''
    while True:
        try:
            player_pointer = int(input(f'{player} : '))
        except ValueError:
            print('please enter a valid number')
        else:
            board,msg = board_validate(board_pointer,board=board,pointer=player_pointer,char=player_pointers[player])
            if not msg:
                player_tracking[player].add(player_pointer)
                if len(player_tracking[player]) >= 3:
                    if win_or_continue(player_tracking[player]):
                        return f'{player} is the winner'
                if not board_pointer:
                    return f'draw! both players well played'
                return board,
            print(msg)


def bot_thinking(board_pointer,bot_set,player_set)-> int:
    '''
    here it will check if there any chance for it to win and proceed with it else looks for the 
    chance the player win in next step if so block it else choose a random pointer from winable combo move

    player set is a set that stores playes moves
    if the move the combo len is 2 that means their next step would be a win 
    with set difference of that missing pointer proceed to return it immediately (either winning or blocking the user)
    '''
    bot_predit = []
    p_length = float('-inf')
    b_length = float('-inf')
    for combo in winning_combo:
        player = combo&player_set
        bot = combo&bot_set
        player_n = len(player)
        if len(bot) >= b_length:
                b_length = len(bot)
                bot_pointer = combo-bot 
                if len(bot_pointer) == 1:
                    temp, = bot_pointer
                    if temp in board_pointer:
                        return temp
                else:
                    bot_predit.append(tuple(bot_pointer))
        else:
            if player_n>=p_length:
                p_length = player_n
                danger_pointer = combo-player
                if len(danger_pointer) == 1:
                    temp, = danger_pointer
                    if temp in board_pointer:
                        return temp

    bot_predit.sort()
    # print(f'{bot_predit = }')
    return random.choice(bot_predit[0])

def single_player(board,board_pointer):
    '''function for single player i.e playing with bot'''
    player1 = input('enter your name : ')
    player2 = 'bot'

    player_pointers = {player1:'X',player2:'O'}
    print(player_pointers)
    print(test_board)
    print('enter the number to fill as per in the board')
    player_tracking = {player1:set(),player2:set()}
    while True:
        res = game_play(player=player1,board_pointer=board_pointer,board=board,player_pointers=player_pointers,player_tracking=player_tracking)

        if isinstance(res,tuple):
            board, = res
        else: 
            if not board_pointer:
                return 'draw!'
            return 'you won!'
        
        player2_pointer = bot_thinking(board_pointer=board_pointer,bot_set=player_tracking[player2],player_set=player_tracking[player1])
        sleep(0.5)
        print(f'{player2} : {player2_pointer}')
        board,msg = board_validate(board_pointer,board=board,pointer=player2_pointer,char=player_pointers[player2])
        player_tracking[player2].add(player2_pointer)
        if len(player_tracking[player1]) >= 3:
            if win_or_continue(player_tracking[player2]):
                return f'you loss!'
            if not board_pointer:
                return f'draw!'


def board_validate(board_p,board,pointer,char):
    '''here is the logic to validate board if the user input(pointer) not in board_pointer => tuple of msg else pop from the
     board pointer '''
    if pointer not in board_p:
        return board,'please fill the un filled area'
    # replace board replaces the _ to the X or O from the board
    board = replace_board(board,board_p[pointer],char)
    board_p.pop(pointer)
    print(board)
    return board,None

def win_or_continue(player_track):
    '''this func checks weather the current player (player1 | player2) won or not'''
    # checks by set intersection if the intersection of the player's move == to any winning combo returns won
    for combo in winning_combo:
        if combo & player_track == combo:
            return 1
    return None

def game(board,board_pointer,multiplayer=None):
    '''this function starts the game either single or multi loop till a player won or draw'''
    if multiplayer:
        player1 = input('enter player 1 name : ')
        player2 = input('enter player 2 name : ')

        player_pointers = {player1:'X',player2:'O'}

        print(player_pointers)
        print(test_board)
        print('enter the number to fill as per in the board')

        player_tracking = {player1:set(),player2:set()}

        while True:

            res = game_play(player=player1,board_pointer=board_pointer,board=board,player_pointers=player_pointers,player_tracking=player_tracking)

            if isinstance(res,tuple):
                board, = res
            else: return res
            
            res = game_play(player=player2,board_pointer=board_pointer,board=board,player_pointers=player_pointers,player_tracking=player_tracking)

            if isinstance(res,tuple):
                board, = res
            else: return res
            
    return single_player(board=board,board_pointer=board_pointer)            

def replace_board(board,index,char):
    '''it replaces the char(_) with the player's char (X | O)'''
    return board[:index]+char+board[index+1:]

def main(option):
    '''main func that runs the game according to the user option'''
    if option not in {'1','2'}:
        return 'please select the valid option'
    board = """
___|___|___
___|___|___
   |   | 
"""
    board_pointer = board_dia.copy()
    
    if option == '2':
        return game(board=board,board_pointer=board_pointer,multiplayer=1)
    return game(board=board,board_pointer=board_pointer)
        

if __name__ == '__main__':
    '''loops till the user select 3 or sends the user input as option to the main func to proceed with the game '''
    print('welcome to the tic tac toe game'.title())
    while True:
        option = input("""
1) single player
2) multiplayer
3) quit
select : """)
        if option == '3': break
        print(main(option))