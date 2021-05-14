import random
import math
import numpy as np


class N_Backtracking:
    def __init__(self,n=4):
        if  type(n)!=np.int:
            raise ValueError("El valor de n debe ser un entero positivo")
        elif  n<4:
            raise ValueError("El valor de n debe ser mayor o igual a 4")
        self.the_board=np.array([[0]*n]*n)
        self.n=n
        
    
    def copy(self):        
        return N_Backtracking(self.parents,self.n)
        
        


def BTSolve4Queens(self, col=0): 
    # Retorno en el llamado recursivo: todas las damas han sido ubicadas en el tablero
    # (de las columnas 0 a 3)
    if col == self.n: 
        return True
  
    # Si no se han ubicado todas las damas, ubicar una nueva dama en las casillas
    # de la columna bajo evaluación (col)
    for i in range(self.n): 
        
        if valid_placement(self, i, col): 
            # Se ubica una nueva dama en la fila i-ésima de esa nueva columna 
            self.the_board[i][col] = 1

            
            # Se hace el llamado recursivo para ubicar el resto de las damas 
            if BTSolve4Queens(self, col + 1) == True: 
                return True
  
            # "else", Si no hubo una solución (el valor de retorno fue falso), quitamos la dama evaluada
            self.the_board[i][col] = 0

    # Si la dama no pudo ser ubicada en una casilla sobre esta columna para todas las combinaciones
    # previas, se retorna "Falso"
    return False

# Escribe la solución en pantalla
# def print_position(self): 
#     for i in range(self.n): 
#         for j in range(self.n): 
#             print (self.parents[i][j], end = " ") 
#         print() 
def print_position(board): 
    n=len(board)
    for i in range(n): 
        for j in range(n): 
            if j==0:
                print ("\t",board[i][j], end = " ") 
            else:
                print (board[i][j], end = " ") 
        print()    

# Evalúa la validez de una nueva posición según las damas puestas a la izquierda
def valid_placement(self, row, col): 
    #Escribe la posición evaluada y devuelve el tablero a su estado inicial
    self.the_board[row][col]=1
    print("Posición evaluada")
    print_position(self.the_board)
    self.the_board[row][col]=0
    
    # Valida que no haya damas en columnas previas a la actual para la misma fila
    for i in range(col): 
        if self.the_board[row][i] == 1: 
            return False
  
    # Valida que no haya damas en la diagonal hacia arriba
    for i in range(row, -1, -1):
        if self.the_board[row-i][col-i] == 1: 
            return False

    # Valida que no haya damas en la diagonal hacia abajo
    for i in range(row, self.n, 1): 
        if col-i<0 or row+i>self.n-1: # previene evaluaciones por fuera del tablero
            break
        if self.the_board[row+i][col-i] == 1: 
            return False

    return True


def Solve_n_Queens(n):
    x=N_Backtracking(n)
    BTSolve4Queens(x)
    