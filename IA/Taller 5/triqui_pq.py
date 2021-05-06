class TriquiState:
    def __init__(self, board, move_i=-1, move_j=-1, alpha=None, beta=None):
        if alpha is not None:
            self.alpha = alpha
        else: 
            self.alpha =-2 # -inf
        if beta is not None:
            self.beta = beta
        else: 
            self.beta = 2   # +inf
        
        self.move_i=move_i
        self.move_j=move_j

        self.board=[['_','_','_'],
                    ['_','_','_'],
                    ['_','_','_']]
        if board is not None:
            for i in range(3):
                for j in range(3):
                    self.board[i][j]=board[i][j]
    
    def terminal(self):
        #Evaluar estado terminal por filas
        for i in range(3): 
            if(self.board[i] == ['X','X','X']):
                return 1
            if(self.board[i] == ['O','O','O']):
                return -1
        
        #Evaluar estado terminal por columnas
        for j in range(3):
            X = 0
            O = 0
            for i in range(3):
                if( self.board[i][j] == 'X'):
                    X = X + 1
                if( self.board[i][j] == 'O'):
                    O = O + 1
            if (X == 3):
                return 1
            elif (O == 3):
                return -1
        
        # Evaluar estado terminal, diagonal 1
        if( self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and self.board[0][0] == 'X' ):
            return 1
        if( self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0] and self.board[0][2] == 'X' ):
            return 1
        
        #Evaluar estado terminal, diagonal 2
        if( self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and self.board[0][0] == 'O' ):
            return -1
        if( self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0] and self.board[0][2] == 'O' ):
            return -1
        
        # Si el tablero esta vacio, se retorna None para continuar el juego.
        for i in range(3):
            for j in range(3):
                if (self.board[i][j] == '_'):
                    return None
        
        # En otro caso, se trata de un empate
        return 0
    
    def get_board(self):
        another_board=[['_','_','_'],
                       ['_','_','_'],
                       ['_','_','_']]
        for i in range(3):
            for j in range(3):
                another_board[i][j] = self.board[i][j]
        return another_board
    
    def print_board(self):
        print("Utilidad:", self.terminal())
        for i in range(0, 3):
            for j in range(0, 3):
                print('{}|'.format(self.board[i][j]), end=" ")
            print()
        print()

        
        
def minimax(state):
    alpha = -2 # equivalente de -inf para el valor de utilidad del triqui
    beta = 2   # equivalente de +inf para el valor de utilidad del triqui
    (v, sel_i, sel_j) = maximize(state, alpha, beta)
    return sel_i, sel_j

def maximize(state, alpha, beta):
    sel_i=None
    sel_j=None
    t=state.terminal()
    if t != None:
        return t, sel_i, sel_j

    children=[]
    board=state.get_board()
    v = -2
    
    # Expande todos los hijos del estado actual y evalúa si maximiza las posibilidades
    # del jugador automático
    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                board[i][j] = 'X'
                children.append(TriquiState(board, i, j, alpha, beta))
                board[i][j] = '_'
    
    for child in children:
#          child.print_board()
        (m, min_i, min_j) = minimize(child, alpha, beta)
        if m > v:
            v = m
            sel_i=child.move_i
            sel_j=child.move_j
            # Se ejecuta la poda si v >= beta
            if v >= beta:
                return v, sel_i, sel_j
            if v > alpha:
                alpha = v
    
    return v, sel_i, sel_j


def minimize(state, alpha, beta):
    sel_i=None
    sel_j=None
    t=state.terminal()
    if t != None:
        return t, sel_i, sel_j

    children=[]
    board=state.get_board()
    v = 2
    
    # Expande todos los hijos del estado actual y evalúa si maximiza las posibilidades
    # del jugador automático
    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                board[i][j] = 'O'
                children.append(TriquiState(board, i, j, alpha, beta))
                board[i][j] = '_'
    
    for child in children:
        #child.print_board()
        (m, max_i, max_j) = maximize(child, alpha, beta)
        if m < v:
            v = m
            sel_i=child.move_i
            sel_j=child.move_j
            # Se ejecuta la poda si v <= alpha
            if v <= alpha:
                return v, sel_i, sel_j
            if v < beta:
                beta = v
    
    return v, sel_i, sel_j
def print_level(the_board):
    print('    0',' 1',' 2')
    for i in range(0, 3):
        for j in range(0, 3):
            if j==0:
                print(i,' ','{}|'.format(the_board[i][j]), end=" ")
            else:
                print('{}|'.format(the_board[i][j]), end=" ")
        print()
    print()
        
        
def terminal_level(self):
        #Evaluar estado terminal por filas
        for i in range(3): 
            if(self[i] == ['X','X','X']):
                return 1
            if(self[i] == ['O','O','O']):
                return -1
        
        #Evaluar estado terminal por columnas
        for j in range(3):
            X = 0
            O = 0
            for i in range(3):
                if( self[i][j] == 'X'):
                    X = X + 1
                if( self[i][j] == 'O'):
                    O = O + 1
            if (X == 3):
                return 1
            elif (O == 3):
                return -1
        
        # Evaluar estado terminal, diagonal 1
        if( self[0][0] == self[1][1] and self[1][1] == self[2][2] and self[0][0] == 'X' ):
            return 1
        if( self[0][2] == self[1][1] and self[1][1] == self[2][0] and self[0][2] == 'X' ):
            return 1
        
        #Evaluar estado terminal, diagonal 2
        if( self[0][0] == self[1][1] and self[1][1] == self[2][2] and self[0][0] == 'O' ):
            return -1
        if( self[0][2] == self[1][1] and self[1][1] == self[2][0] and self[0][2] == 'O' ):
            return -1
        
        # Si el tablero esta vacio, se retorna None para continuar el juego.
        for i in range(3):
            for j in range(3):
                if (self[i][j] == '_'):
                    return None
        
        # En otro caso, se trata de un empate
        return 0
    
    
def jugada_bot(the_board):
    initial_state=TriquiState(the_board)
    sel_i,sel_j=minimax(initial_state)
    the_board[sel_i][sel_j]='X'
    return the_board


def jugada_usuario(the_board):
    i=int(input('fila(0-3):'))
    j=int(input('columna(0-3):'))
    if the_board[i][j]=='_':
        the_board[i][j]='O'
    else:
        print('Celda ya ocupada')
        jugada_usuario(the_board)
        
    return the_board
def play_game(the_board):
    a=terminal_level(the_board)
    
    while a==None:
        the_board=jugada_bot(the_board)
        print('Automatico :\n ')
        print_level(the_board)
        a=terminal_level(the_board)
        if a==0:
            return print('Empate')
        elif a==-1:
            return print('Ganador Usuario ')
        elif a==1:
            return print('Ganador IA ')
        
        the_board=jugada_usuario(the_board)
        print('Usuario :\n ')
        print_level(the_board)
        a=terminal_level(the_board)
        if a==0:
            return print('Empate')
            
        elif a==-1:
            return print('Ganador Usuario ')
        elif a==1:
            return print('Ganador IA ')
        
def play_game_2(the_board):
    inicia=int (input('Quien desea que comience? (0:Automatico, 1:Usted): '))
    a=terminal_level(the_board)
    
    while a==None:
        if inicia==0:
            the_board=jugada_bot(the_board)
            print('Automatico :\n ')
            print_level(the_board)
            a=terminal_level(the_board)
            if a==0:
                return print('Empate')
            elif a==-1:
                return print('Ganador Usuario ')
            elif a==1:
                return print('Ganador IA ')
            else:
                inicia=1
        if inicia==1:
            the_board=jugada_usuario(the_board)
            print('Usuario :\n ')
            print_level(the_board)
            a=terminal_level(the_board)
            if a==0:
                return print('Empate')
            elif a==-1:
                return print('Ganador Usuario ')
            elif a==1:
                return print('Ganador IA ')
            else:
                inicia=0

  