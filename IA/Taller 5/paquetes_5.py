import random
import math

class KSState:
    def __init__(self, limit, initial_package=None):
        self.limit=limit
        if initial_package is not None:
            self.packages=[initialPackage]
            self.load=initialPackage[0]
            self.value=initialPackage[1]
            self.num_packages=1
        else:
            self.packages=[]
            self.load=0
            self.value=0
            self.num_packages=0

    ## Actualiza el estado para incluir el siguiente paquete seleccionado
    def updateState(self,package):
        self.packages.append(package)
        self.load=self.load + package[1][0]
        self.value=self.value + package[1][1]
        self.num_packages=self.num_packages+1


class KSHillClimbingSolver:
    def __init__(self, state, task_packages):
        self.state=state
        self.task_packages=task_packages
        
    ## Expande los posibles estados sucesores del estado actual. 
    ## La poda se efectúa aquí mismo
    def pruned_successors(self):
        successors_dict={}
        for key, package in self.task_packages.items():
            ## Solo agrega a la lista de candidatos aquellos paquetes que no violan
            if self.state.load+package[0] <= self.state.limit:
                successors_dict[key]=package
        return successors_dict
        
    ## Escoge el mejor paquete entre aquellos que pueden generar un nuevo estado válido
    ## y lo borra de la lista inicial de paquetes (task_packages)
    def choose_best(self,packages):
        max_value=-1
        chosen=None
        for key, package in packages.items():
            if (package[0]/package[1])>max_value:
                chosen_key=key
                chosen_package=package
                max_value=(package[0]/package[1])
        ## Se retira el paquete seleccionado de la lista de pendientes
        borrado=self.task_packages.pop(chosen_key)
        return chosen_key, chosen_package
        
    ## Solucional el "problema de la mochila" usando "Hill Climbing"
    def hcSolve(self):
        end_loop=False
        iteration=0;
        while end_loop==False:
            neighbours=self.pruned_successors()
            print("Paquetes disponibles en la iteración", iteration, ": ", self.task_packages)
            print("Paquetes candidatos a agregar a los vecinos en la iteración", iteration, ": " ,neighbours)
            if(len(neighbours)>0):
                best_neighbour=self.choose_best(neighbours)
                print("\n El mejor vecino es: ",best_neighbour,'\n')
                self.state.updateState(best_neighbour)
            else:
                end_loop=True
            neighbours.clear()
            iteration=iteration+1
        return self.state   
   
   
def KSHillClimbingExecute(task_packages,initial):
    initial_state=KSState(initial)
    solver=KSHillClimbingSolver(initial_state,task_packages)
    solver.hcSolve()
    print("\n Carga= ",solver.state.load,"Valor= ", solver.state.value )
    print(solver.state.packages)
    print('\n Paquetes sin cargar')
    print(solver.task_packages)
    
    
    
##########################################################
# Clase para representar un paquete en Simulated Annealing
class KSPackageSA:
    def __init__(self, package_label, weight, value):
        self.package_label=package_label
        self.value=value
        self.weight=weight
    
    def __str__(self):
        return str(self.package_label)+" "+str(self.value)+" "+str(self.weight)
    ## Comparar entre valores de paquetes en el "problema de la mochila"
    def __le__(self, other_package):
        return self.value <= other_package.value

#####################################################
# Clase del estado de la mochila para Simulated Annealing
class KSStateSA:
    def __init__(self, previous_state=None, added_package=None):
        # Si no hay estado previo, inicializa la mochila como vacía
        if previous_state is None:
            self.packages=[]
            self.num_packages=0
            self.load=0
            self.value=-1
        else: # pero si existe estado previo,copia sus paquetes
            self.packages=previous_state.packages.copy()
            self.num_packages=previous_state.num_packages
            self.load=previous_state.load
            self.value=previous_state.value
            ############################################################
            ## En caso de que se construya un estado para expansión de
            ## vecinos, se agrega el nuevo paquete al estado existente
            if added_package is not None:
                self.packages.append(added_package)
                self.num_packages=self.num_packages+1
                self.load=self.load+added_package.weight
                self.value=self.value+added_package.value
    
    def __str__(self):
        string=""
        for p in self.packages:
            string=string + " - "+str(p)
        return string


    ## Actualiza el estado para incluir el siguiente paquete seleccionado
    def updateState(self, package):
        self.packages.append(package)
        self.load=self.load + package.weight
        self.value=self.value + package.value
        self.num_packages=self.num_packages+1
        
        
        
  


class KSSimulatedAnnealingSolver:
    def __init__(self, initial_state, limit, task_packages, initial_temp=1, delta_temp=0.05, final_temp=0, random_walk_length=1):
            self.state=initial_state
            self.limit=limit
            self.task_packages=task_packages
            self.initial_temp=initial_temp
            self.delta_temp=delta_temp
            self.final_temp=final_temp
            self.random_walk_length=random_walk_length
            
    #########################################
    ## Retorna una lista de KSPackageSA vecinos
    def expand_state(self):
        state_neighbours=[]
        print("Los estados vecinos son: ")
        for p in self.task_packages:
            new_state=KSStateSA(previous_state=self.state, added_package=p)
            # Evita que se agreguen estados vecinos no viables, respetando el límite
            if new_state.load <= self.limit:
                state_neighbours.append(new_state)
                print(new_state)
        return state_neighbours
    
    def remove_selected_package(self, state):
        label=state.packages[-1].package_label
        for i in range (0,len(self.task_packages)):
            if self.task_packages[i].package_label==label:
                print ("Removiendo paquete", label, "con valor:", self.task_packages[i].value)
                del self.task_packages[i]
                return
    
    def simulated_annealing(self):
        temp = self.initial_temp

        # Start by initializing the current state with the initial state
        # solution = self.state

        ## Bucle principal
        while temp > self.final_temp:
            ############################################
            ## Expandir el estado actual
            neighbours=self.expand_state()
            
            # Si no quedan vecinos viables por agregar, retorna la solución actual
            if (len(neighbours)==0):
                return self.state

            print ("T: ", temp)
            for i in range(0,self.random_walk_length):
                ############################################
                ## Seleccionar un estado vecino al azar
                selected_neighbour = random.choice(neighbours)

                #####################################################
                # Verificar si el vecino es el mejor hasta el momento
               
                delta_E = (self.state.load/self.state.value)-(selected_neighbour.load/selected_neighbour.value)
                

                # si la nueva solución es mejor (y cumple las restricciones), tomarla
                if delta_E < 0:
                    self.state = selected_neighbour

                # si la nueva solución no es mejor, aceptarla con probabilidad de e^(-costo/temperatura)
                else:
                    if random.uniform(0, 1) < math.exp(-abs(delta_E) / temp):
                        self.state = selected_neighbour

            self.remove_selected_package(selected_neighbour)
            print("Nueva lista de paquetes de trabajo")
            for p in self.task_packages:
                print(p)
            
            # decrement the temperature
            temp -= self.delta_temp

        return self.state
    
def KSSimulatedAnnealingExecute(initial_state,initial,ks_packages):
    
    solver=KSSimulatedAnnealingSolver(initial_state, initial, ks_packages)
    ks_solution=solver.simulated_annealing()
    print("La solución es:")
    for p in ks_solution.packages:
        print(p)
        
import numpy as np
import random

class N_Damas:
    def __init__(self,parents=None , n=4):
        if n<4:
            raise ValueError("El valor de n debe ser mayor o igual a 4")
        elif  type(n)!=np.int:
            raise ValueError("El valor de n debe ser un entero positivo")
        self.the_board=np.array([[0]*n]*n)
        self.n=n
        if (parents is not None) and (len(parents)<2):
            raise ValueError("Deben ser mínimo dos cromosomas padres")
        if parents is None:
            parent_1=random_parent(n)
            parent_2=random_parent(n)
            #(parent_1==parent_2).all()
            parents=[parent_1,parent_2]
        self.parents=parents
    
    def copy(self):        
        return N_Damas(self.parents,self.n)
        
        
def random_parent(n=4):
    parent=np.array([[0]*n]*n)
    row=list(range(n))
    col=list(range(n))
    for i in range(n):
        random_row=random.choice(row)
        random_col=random.choice(col)
        parent[random_row][random_col]=1
        row.remove(random_row)
        col.remove(random_col)
    return parent

def buscar_casillas(board):
    l_casillas=[]
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j]==1:
                l_casillas.append((i,j))
    return l_casillas

def num_attacks(board):
    n=len(board)
    board_copy=board.copy()
    attacks=0
    while len(buscar_casillas(board_copy))!=0:
        l_casillas=buscar_casillas(board_copy)
        row=l_casillas[0][0]
        col=l_casillas[0][1]       
        if board_copy[row][col]!=1:
            print(f"ERROR en las posición {row,col}")
            print_position(board_copy)
            return attacks
        board_copy[row][col]=0

        # Suma los ataques si hay damas en columnas para la misma fila
        for i in range(n): 
            if board_copy[row][i] == 1: 
                attacks+=1
        # Suma los ataques si hay damas en filas para la misma columna     
        for i in range(n): 
            if board_copy[i][col] == 1: 
                attacks+=1
        # suma los ataques si hay damas en las diagonales
        for i in range(n):
            if (row+i) in range(n):
                if ((col+i) in range(n)) and (board_copy[row+i][col+i] == 1):
                    attacks+=1
                if ((col-i) in range(n)) and (board_copy[row+i][col-i] == 1):
                    attacks+=1
            if ((col+i) in range(n)) and ((row-i) in range(n)) and (board_copy[row-i][col+i] == 1):
                attacks+=1
            if ((col-i) in range(n)) and ((row-i) in range(n)) and (board_copy[row-i][col-i] == 1):
                attacks+=1
    return attacks

# Escribe la solución en pantalla
def print_position(board): 
    n=len(board)
    for i in range(n): 
        for j in range(n): 
            if j==0:
                print ("\t",board[i][j], end = " ") 
            else:
                print (board[i][j], end = " ") 
        print()    
        
def hijos(parent_1,parent_2,division):
    n=len(parent_1)
    hijo_1=parent_1.copy()
    hijo_2=parent_2.copy()
    for row in range(n):
        for col in range(n):
            if col>division:
                hijo_2[row][col]=parent_1[row][col]
                hijo_1[row][col]=parent_2[row][col]               
    return [hijo_1,hijo_2]

def mutar_hijo(hijo_inicial):
    hijo=hijo_inicial.copy()
    n=len(hijo)
    valor=random.choice(range(n))
    col_modif=random.choice(range(n))
    for row in range(n):
        hijo[row][col_modif]=0
    hijo[valor][col_modif]=1
    #print(f"Fila: {valor}, columna: {col_modif}")
    return hijo

def solve_genetic(N_Damas,division=1):
    n=N_Damas.n
    n_parent=1
    generacion=1
    print(f"Generación: {generacion}\n")
    for parent in N_Damas.parents:
        if num_attacks(parent)==0:
            print("La solución es:")
            print(f"********Padre {n_parent}:")
            print_position(parent)
            return
        else:
            print(f"Padre {n_parent}:")
            print_position(parent)
        n_parent+=1  
    control=True  
    N_Damas_copy=N_Damas.copy()
    while control:
        Hijos=hijos(N_Damas_copy.parents[0],N_Damas_copy.parents[1],division)
        mutacion_Hijos=[]
        generacion+=1
        n_hijo=1
        print(f"Generación: {generacion}\n")
        for hijo in Hijos:
            if num_attacks(hijo)==0:
                print("La solución es:")
                print(f"********Hijo {n_hijo}:")
                print_position(hijo)
                control=False
                return
            else:
                print(f"Hijo {n_hijo}:")
                print_position(hijo)
                m_hijo=mutar_hijo(hijo)
                print(f"\tHijo mutado:")
                print_position(m_hijo)
                mutacion_Hijos.append(m_hijo)                
            n_hijo+=1
        
        N_Damas_copy.parents=mutacion_Hijos   
    