import random
possiblewins = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8],
                [3, 6, 9], [1, 5, 9], [3, 5, 7]]
tokens = ['X', 'O']

class board:
    def __init__(self, p1, p2):
        self.players = [p1, p2]
        random.shuffle(self.players)  # Random player start
        self.occupied = list()  # List of occupied slots
        self.boardtemplate = ('''
          1  |  2  |  3
        -----|-----|-----
          4  |  5  |  6
        -----|-----|-----
          7  |  8  |  9  \n''')
        self.board = self.boardtemplate

    def updateboard(self, move, p):
        '''Occupy and update board.'''
        self.occupied.append(move)
        self.board = self.board.replace(str(move), p.token)

    def possiblemoves(self):
        '''Return a list of possible moves.'''
        pos = list()
        for i in range(1,10):
            if i in self.occupied: continue
            pos.append(i)
        return pos

    def resetboard(self):
        '''Resets the board.'''
        self.board = self.boardtemplate
        self.occupied = list()
        random.shuffle(self.players)


class player:
    def __init__(self, name, chosentoken):
        self.name = name
        self.token = self.validtoken(chosentoken)
        self.score = 0
        self.moves = list()
        self.curmove = None

    def resetscore(self):
        self.score = 0

    def won(self):
        self.score += 1

    def generatemove(self, board):  # Generate move for AI
        move = None
        while move is None:
            try:
                move = random.choice(board.possiblemoves())
            except IndexError:
                print('draw')
        return move

    def validtoken(self, token):
        global tokens
        token = token.upper()
        if token not in tokens:
            raise Exception('ERROR: Invalid token - X/O')
        else:
            return token
    
    def setmove(self, move):
        self.moves.append(move)


def checkvalidmove(move, board):
    try:
        move = int(move)  # Sanity check
    except ValueError:
        print('ERROR: Move must be an integer.', move)
        return False
    if move not in range(1, 10):
        print('ERROR: Move value must be within 1-9.')
        return False
    if move not in board.possiblemoves():
        print(move, 'already occupied.')
        return False
    else:
        return True

def checkwinner(p1, p2):  # Passed arg - players
    global possiblewins
    moves_both = {p1: p1.moves, p2: p2.moves}
    for curplayer in moves_both:
        for wins in possiblewins:
            count = 0
            for mov in moves_both[curplayer]:
                if mov in wins:
                    count += 1
                if count == 3:
                    return curplayer
    return None

def askmove(board, player):
    moveofplayer = None
    while moveofplayer is None:
        if player.name.startswith('AI') or player.name.startswith('ai'):
            moveofplayer = player.generatemove(board)
        else:
            moveofplayer = input('Input move (1-9): ')
        if not checkvalidmove(moveofplayer, board):
            moveofplayer = None
    return int(moveofplayer)

def game(player1, player2):
    p1 = player(name1, 'X')
    p2 = player(name2, 'O')
    tictactoe = board(p1, p2)
    players = tictactoe.players
    print(f'Player {players[0].name} goes first!')
    print(tictactoe.board)
    winner = None
    while winner is None:
        for p in players:
            test = tictactoe.possiblemoves()
            if len(test) < 1 :
                winner = 'Draw'
                break
            pmove = askmove(tictactoe, p)
            p.curmove = pmove
            p.setmove(pmove)
            tictactoe.updateboard(pmove, p)
            print(tictactoe.board)
            winner = checkwinner(p1, p2)
            if winner is not None or winner == 'Draw':
                break
    if winner != 'Draw':
        print(f'Winner - {winner.name}.')
        winner.won()  # add one to winner's score
    else:
        print('It\'s a draw!')
    tictactoe.resetboard()


if __name__ == "__main__":
    print('Welcome to Tic-Tac-Toe!')
    print('Enter your move based on the numbers on the board.')
    # input('Press any key to play.')
    name1 = input('Enter Player 1\'s name: ')
    name2 = input('Enter Player 2\'s name: ')
    while True:
        game(name1, name2)
        inp = input('Press any key to play again. \'Quit\' to quit.\n')
        if inp.lower() == 'quit':
            quit()
