#index.py (Tic-Tac-Toe [Web App] )
#author: tom mulvey
#date : 12/11
#vers 1.1
#purpose : web app intro + some html / css
# beware of spaghetti code below

from app import app
from flask import request, session, render_template

@app.route('/')
def index():
    return "Hello. This is the index page. Check out /ttt , dawg"

@app.route('/ttt')
def ttt():
    '''
    The game will look for a board, comp_guess, and player_guess.
    Vers 1 : Player 1 selects their spot. Game checks if player won.
             Computer will then copy the board, find best spot, them play.
             Check game status again.

    only the player can go first. no pvp, only pvc. Can improve later
    figure out printing, then the rest is very similar to lab 10s TTT game

    ALSO change the input button to buttons on the map that black out once pressed.
    this is a really bodged program that stinkz //done

    12/11 basically done program besides keeping fix positions of boxes
    regardless of the text in it. Easy fix i can do some other time.
    also the user can robably breaking the game by messing around with
    the URL. say if they take a spot then also type spot=x and x is
    one of comps spots. can fix some other time
    '''
    #board = {1:'', 2:'', 3:'', 4:'', 5:'', 6:'', 7:'', 8:'', 9:''}
    #check if curent game is on
    if "board" in session :
        board = session["board"]
    else:
        board = {1:'', 2:'', 3:'', 4:'', 5:'', 6:'', 7:'', 8:'', 9:''}
        player = [ ]
    # try sorting dictionary then passing ? //Didnt work...jinja2 sort time
    result = None
    if 'spot' in request.args :
        spot = request.args["spot"]
        if spot in board:
            board[spot] = '☺'
        check = is_board_full(board)
        if check == True :
            result = "tie"
        result = check_game_status(spot, board)

    if "reset" in request.args :
        board = {'1':'', '2':'', '3':'', '4':'', '5':'', '6':'', '7':'', '8':'', '9':''}

    #computer move
    #print(board, "THIS IS WHAT IM SENDING")
    if result == "human u won" or result == "tie" :
        print("nothing will change.")
    else :
        comp_spot = computer_move(board)
        board[str(comp_spot)] = 'X'
        result = check_game_status(comp_spot, board)

    print(result)
    l = sorted(board.items())
    board = {}
    print(l)
    for ts in l : #tuples in list L, l is sorted elemtns of board
        board[int(ts[0])] = ts[1]
    print(board)
    #this is me sorting the dictionary before passing it
    #     i was having troubles where the board would randomly
    #     unsort in the jinja and i thought I could bypass it
    #     by sorting it first, ill leave it to leave my mark on
    #     this bodging mess
    #I send the sorted board and it comes back unsorted...

    #save to sesh
    session["board"] = board
    return render_template('tictacog.html', board=board, result=result)


app.secret_key = '324iu234oiu124iu214io12u42i214iou12'


#functtions for TTT game.
def check_game_status(position, board) :
    #all possible directions to win
    row_list = [ [1,2,3], [4,5,6], [7,8,9] ]
    col_list = [ [1,4,7], [2,5,8], [3,6,9] ]
    slant_list = [ [1,5,9], [3,5,7] ]
    #given position of last placed item,
    #check its row, col, and slant.
    #if all 3 are the same, that player won
    for rows in row_list :
        if int(position) in rows :
            if board[str(rows[0])] == board[str(rows[1])] == board[str(rows[2])] :
                if board[str(rows[0])] == 'X' :
                    return "computer has won"
                else :
                    return "human u won"

    for cols in col_list :
        if int(position) in cols :
            if board[str(cols[0])] == board[str(cols[1])] == board[str(cols[2])] :
                if board[str(cols[0])] == 'X' :
                    return "computer has won"
                else :
                    return "human u won"

    for slants in slant_list :
        if int(position) in slants :
            if board[str(slants[0])] == board[str(slants[1])] == board[str(slants[2])] :
                if board[str(slants[0])] == 'X' :
                    return "computer has won"
                elif board[str(slants[0])] == '☺' :
                    return "human u won"
                else :
                    return

    return

def is_board_full(board):
    empty = ''
    return not any(spot == empty for spot in board.values()) #if +1 spot is not empty, returns false, otherwise true

def computer_move(board):
    # "ai" moves
    # check if cpu can wins
    # block human
    # should dd forking here, but i do not want unbeatable.
    # corner
    # side

    def clone_board (board) :
        return board.copy()

    def test_win_spot (board, char, i) :
        #char is ☺ or X, i is index of Board
        comp_board = clone_board(board)
        comp_board[i] = char
        return check_game_status(i, comp_board)
    #see if comp can win
    for i in range(1,10) :
        if board[str(i)] == '' and test_win_spot(board, 'X', i) == "computer has won" :
            return i
    #block human
    for i in range(1,10) :
        if board[str(i)] == '' and test_win_spot(board, '☺', i) == "computer has won" :
            return i
    #play a corner
    for i in [1,3,7,9] :
        if board[str(i)] == '' :
            return i
    # center
    if board['5'] == '' :
        return 5
    # play the sidez
    for i in [2,4,6,8] :
        if board[str(i)] == '' :
            return i
