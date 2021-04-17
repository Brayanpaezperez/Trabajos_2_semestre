# Definición de la clase de Estado en el Puzzle de 8 casillas
import numpy as np
    
class Puzzle8_State:
    def __init__(self, parent, label, positions=[], heuristic_val=-1, move=0,level=0):
        self.parent=parent
        self.label=label
        self.level=level
        self.solution=np.arange(1,10).reshape(3,3)
        self.solution[2][2]=0
        if positions==[]:
            self.positions=np.arange(1,10).reshape(3,3)
            self.positions[2][2]=0
        else:
            self.positions=positions
        self.heuristic_val=heuristic_val # En este caso, la cantidad de casillas desordenadas
        self.expanded_states=[] # Children
    
    def __lt__(self, other):
        if(self.heuristic_val<other.heuristic_val):
            return True
        else:
            return False
    
    def getPosition(self):  
        return self.positions
    
    def setPosition(self,positions):  
        self.positions=positions
    
    def addExpandedState(self,state):
        self.expanded_states.append(state)
    
    def is_goal(self):
        comparison=True
        for i in range (3):
            for j in range (3):
                if self.positions[i][j]!=self.solution[i][j]:
                    comparison=False
                    break
        return comparison
    
   
## Buscar la casilla vacía para poder aplicar una transición (jugada del puzzle)

def search_empty (matrix):
    for i in range (3):
        for j in range (3):
            if matrix[i][j]==0:
                return i,j
    return -1,-1

##################################################
# Definir las movidas del puzzle de 8 casillas 
# (Sentido contrario a las manecillas del reloj)

## Mover arriba
def move1(position, empty_i, empty_j):
    result=np.arange(1,10).reshape(3,3)
    for i in range (3):
        for j in range (3):
            result[i][j] = position[i][j]
    exchange_value=position[empty_i-1][empty_j]
    result[empty_i][empty_j]=exchange_value
    result[empty_i-1][empty_j]=0
    return result

## Mover a la izquierda
def move2(position, empty_i, empty_j):
    result=np.arange(1,10).reshape(3,3)
    for i in range (3):
        for j in range (3):
            result[i][j] = position[i][j]
    exchange_value=position[empty_i][empty_j-1]
    result[empty_i][empty_j]=exchange_value
    result[empty_i][empty_j-1]=0
    return result
    
## Mover abajo 
def move3(position, empty_i, empty_j):
    result=np.arange(1,10).reshape(3,3)
    for i in range (3):
        for j in range (3):
            result[i][j] = position[i][j]
    exchange_value=position[empty_i+1][empty_j]
    result[empty_i][empty_j]=exchange_value
    result[empty_i+1][empty_j]=0
    return result

## Mover a la derecha
def move4(position, empty_i, empty_j):
    result=np.arange(1,10).reshape(3,3)
    for i in range (3):
        for j in range (3):
            result[i][j] = position[i][j]
    exchange_value=position[empty_i][empty_j+1]
    result[empty_i][empty_j]=exchange_value
    result[empty_i][empty_j+1]=0
    return result

# Comprobar si dos estados posiciones son iguales
def are_equal_states(position1, position2):
    return np.array_equal(position1,position2)
    
# Verificar si un estado ya ha sido visitado (lista de matrices)
def already_visited(state, visited_states):
    for t in visited_states:
        if are_equal_states(state, t):
            return True
    return False

def Search_states(inicial_state,label):
    childs=[]
    labels=[]
    if inicial_state.expanded_states is None:
        return None
    else:
        for child in inicial_state.expanded_states:
            childs.append(child)
            labels.append(child.label)
    if label in labels:
        return inicial_state
    for child in childs:
        state=Search_states(child,label)
        if state!=None:
            return state
    return None 
##################################################################
## Cálculo de la Heurística 
## heurística propuesta para el puzzle de 8 casillas
def heuristic(state):
    h_val=0
    for i in range (3):
        for j in range (3):
            if state.positions[i][j]!=state.solution[i][j]:
                h_val=h_val+1
    return h_val  

def heuristic_manh(state):
    h_val=0
    for i_s in range (3):
        for j_s in range (3):
            for i in range (3):
                for j in range (3):
                    if state.positions[i_s][j_s]==state.solution[i][j]:
                        h_val=abs(i_s-i)+abs(j_s-j)
    return h_val  

from queue import PriorityQueue ## Se usa una cola de prioridad
  
    
  
    
#############################################################################################################################
#################################################### Codigos ####################################################
#############################################################################################################################
  
    
    
###########################################################################
########################### Búsqueda en anchura ###########################
###########################################################################

def Puzzle8_breadthfirst(initial_state):
    if initial_state is None:
        return
    visit_queue=[]
    visit_queue.append(initial_state)
    visited_states=[]
    label=1
    while (len(visit_queue)>0):
        t=visit_queue.pop(0) 
        visited_states.append(t.getPosition())
        if t.is_goal() == True:
#             print("\nEl estado solución es: "+str(t.label))
#             print(t.getPosition())
            l_states=[t]
            label=t.label
            while label!=initial_state.label:
                state=Search_states(initial_state,label)
                if state is not None:
                    label=state.label
                    l_states.append(state)
            n=len(l_states)
            print('\n Metodo: Busqueda en Anchura \n Pasos a seguir para hallar la solución \n ')
            for i in range(n):
                print(l_states[n-i-1].getPosition(),l_states[n-1-i].label, "\t paso:",i, "\n")
            return t
        else:
#             print("Visité el estado "+str(t.label)+", pero no es solución")
#             print(t.getPosition())
            ########################
            ## Expandir el nodo t ##
            ########################
            empty_position=search_empty(t.getPosition())
            if(empty_position[0]>0):
                new_pos_u=move1(t.getPosition(),empty_position[0],empty_position[1])
                if already_visited(new_pos_u,visited_states)==False:
                    visited_states.append(new_pos_u)                    
                    t.addExpandedState(Puzzle8_State(t,label,new_pos_u,level=t.level+1))
                    label=label+1
            if(empty_position[1]>0):
                new_pos_l=move2(t.getPosition(),empty_position[0],empty_position[1])
                if(already_visited(new_pos_l,visited_states)==False):
                    visited_states.append(new_pos_l)
                    t.addExpandedState(Puzzle8_State(t,label,new_pos_l,level=t.level+1))
                    label=label+1
            if(empty_position[0]<2):
                new_pos_d=move3(t.getPosition(),empty_position[0],empty_position[1])
                if(already_visited(new_pos_d,visited_states)==False):
                    visited_states.append(new_pos_d)
                    t.addExpandedState(Puzzle8_State(t,label,new_pos_d,level=t.level+1))
                    label=label+1
            if(empty_position[1]<2):
                new_pos_r=move4(t.getPosition(),empty_position[0],empty_position[1])
                if(already_visited(new_pos_r,visited_states)==False):
                    visited_states.append(new_pos_r)
                    t.addExpandedState(Puzzle8_State(t,label,new_pos_r,level=t.level+1))
                    label=label+1
            if t.expanded_states is not None:
                for child in t.expanded_states:
                    visit_queue.append(child)
    return "failure"


def primero_anchura(pz):
    puzzleBB=Puzzle8_State(None,0,pz.getPosition())
    return Puzzle8_breadthfirst(puzzleBB)


#####################################################################################################
##############################  Búsqueda en profundidad iterada ID-DLS ##############################
#####################################################################################################

#####
def generar_hijos(t,limit):
    global label
    global visited_states
    empty_position=search_empty(t.getPosition())
    if limit == 0:
        return t
    else:
        if(empty_position[0]>0): # solo se mueve arriba si la posición vacía no está en la primera fila
                new_pos_u=move1(t.getPosition(),empty_position[0],empty_position[1])
                if already_visited(new_pos_u,visited_states)==False:
                    new_state_u=Puzzle8_State(t,label,new_pos_u,level=t.level+1)
                    new_state_u.heuristic_val=heuristic(new_state_u)
                    t.addExpandedState(new_state_u)
                    label=label+1
            
        # Mover a la izquierda
        if(empty_position[1]>0):
            new_pos_l=move2(t.getPosition(),empty_position[0],empty_position[1])
            if already_visited(new_pos_l,visited_states)==False:
                new_state_l=Puzzle8_State(t,label,new_pos_l,level=t.level+1)
                new_state_l.heuristic_val=heuristic(new_state_l)
                t.addExpandedState(new_state_l)
                label=label+1

        # Mover abajo
        if(empty_position[0]<2):
            new_pos_d=move3(t.getPosition(),empty_position[0],empty_position[1])
            if already_visited(new_pos_d,visited_states)==False:
                new_state_d=Puzzle8_State(t,label,new_pos_d,level=t.level+1)
                new_state_d.heuristic_val=heuristic(new_state_d)
                t.addExpandedState(new_state_d)
                label=label+1

        # Mover a la derecha
        if(empty_position[1]<2):
            new_pos_r=move4(t.getPosition(),empty_position[0],empty_position[1])
            if already_visited(new_pos_r,visited_states)==False:
                new_state_r=Puzzle8_State(t,label,new_pos_r,level=t.level+1)
                new_state_r.heuristic_val=heuristic(new_state_r)
                t.addExpandedState(new_state_r)
                label=label+1
        return t
    
def Puzzle8_depthfirst_limit_i(initial_state,limit):
    global end_recursion
    global visited_states
    global label
    t=initial_state
    if end_recursion == True:
        return "success",t
    elif initial_state is None:
        return 'fallo',t
    elif limit == 0:
        return "error_corte",t 
    
    if len(visited_states)==0:
        visited_states.append(initial_state.getPosition())
    
    if t.is_goal() == True:
        print("\nEl estado solución es: "+str(t.label))
        print(t.getPosition())
        end_recursion = True
        return 'success',t
    else:
        #print("Evaluamos el estado "+str(t.label)+", pero no es solución",' limite ',limit)
        #print(t.getPosition())
        ocurrio_corte=False
        t=generar_hijos(t,limit-1)
        if (t.expanded_states is not None):
            for child in t.expanded_states:
                result=Puzzle8_depthfirst_limit_i(child,limit-1)
                if result == "fallo":
                    print("Se termina esta rama con error: " + result)     
                    return result,t
                elif result == "error_corte":
                    ocurrio_corte=True
            if ocurrio_corte:
                return "error_corte",t
        if end_recursion:
            return "success",t
        else:
            return "seguir",t
            
def Puzzle8_depthfirst_limit_2(pz,lt):
    global visited_states
    global end_recursion
    global label
    visited_states=[]
    end_recursion=False
    label=1
    puzzleBB=Puzzle8_State(None,0,pz.getPosition())
    
    return Puzzle8_depthfirst_limit_i(puzzleBB,lt)
    
def ID_DFS(t, max_level):
    
    for limit_level in range(0,max_level+1):
        
        result,t=Puzzle8_depthfirst_limit_2(t,limit_level+1)
        print("El resultado para esta iteración ",limit_level,' es :',result)
        if result=="fallo": 
            print("No se pudo encontrar una respuesta")
            return "fallo",'fallo'
        elif result=="success":
            return t,limit_level
        
    if result=="error_corte":
        print("No se pudo encontrar una respuesta hasta el nivel ", max_level)
        result="fallo_corte"
    return   
        


########################################################################################################
################################ Búsqueda «primero el mejor » (Informada) ###############################
########################################################################################################
#Solución del puzzle de 8 casillas mediante búsqueda en primero el mejor (informada)
def Puzzle8_bestfirst_inf(initial_state):
    if initial_state is None:
        return "failure"
    visited_states=[]
    S=PriorityQueue()
    S.put((initial_state.heuristic_val,initial_state))
    
    label=1
    while not S.empty():
        t=S.get(0)[1]
        print (t.positions)
        
        if t.is_goal() == True:
            print("\nEl estado solución es: "+str(t.label))
            print(t.getPosition())
            return t
        else:
            visited_states.append(t.getPosition())
            print("Visité el estado "+str(t.label)+", pero no es solución")
            print(t.getPosition())
            
            ##########################
            ## Se expande el nodo t ##
            ##########################
            # Se busca la posición de la casilla vacía
            # empty_position[0] es la coordenada x,  empty_position[1] es la coordenada y 
            empty_position=search_empty(t.getPosition()) 
            
            # Se generan todos los estados viables a partir del estado actual que no hayan sido visitados previamente
            # Mover arriba
            if(empty_position[0]>0): # solo se mueve arriba si la posición vacía no está en la primera fila
                new_pos_u=move1(t.getPosition(),empty_position[0],empty_position[1])
                if already_visited(new_pos_u,visited_states)==False:
                    new_state_u=Puzzle8_State(t,label,new_pos_u,level=t.level+1)
                    new_state_u.heuristic_val=heuristic(new_state_u)
                    t.addExpandedState(new_state_u)
                    label=label+1
            
            # Mover a la izquierda
            if(empty_position[1]>0):
                new_pos_l=move2(t.getPosition(),empty_position[0],empty_position[1])
                if already_visited(new_pos_l,visited_states)==False:
                    new_state_l=Puzzle8_State(t,label,new_pos_l,level=t.level+1)
                    new_state_l.heuristic_val=heuristic(new_state_l)
                    t.addExpandedState(new_state_l)
                    label=label+1
            
            # Mover abajo
            if(empty_position[0]<2):
                new_pos_d=move3(t.getPosition(),empty_position[0],empty_position[1])
                if already_visited(new_pos_d,visited_states)==False:
                    new_state_d=Puzzle8_State(t,label,new_pos_d,level=t.level+1)
                    new_state_d.heuristic_val=heuristic(new_state_d)
                    t.addExpandedState(new_state_d)
                    label=label+1
            
            # Mover a la derecha
            if(empty_position[1]<2):
                new_pos_r=move4(t.getPosition(),empty_position[0],empty_position[1])
                if already_visited(new_pos_r,visited_states)==False:
                    new_state_r=Puzzle8_State(t,label,new_pos_r,level=t.level+1)
                    new_state_r.heuristic_val=heuristic(new_state_r)
                    t.addExpandedState(new_state_r)
                    label=label+1
            
            ########################################################
            ## Se agregan los hijos de t a la cola de prioridades ##
            ########################################################
            if t.expanded_states is not None:
                for child in t.expanded_states:
                    h=child.heuristic_val
                    S.put((h,child))
    return "failure"

########################################################################################################
################################ Búsqueda «A* » (Informada) ###############################
########################################################################################################
def Puzzle8_AA_(initial_state):
    if initial_state is None:
        return "failure"
    visited_states=[]
    S=PriorityQueue()
    S.put((initial_state.heuristic_val,initial_state))
    
    label=1
    while not S.empty():
        t=S.get(0)[1]
        print (t.positions)
        
        if t.is_goal() == True:
            print("\nEl estado solución es: "+str(t.label))
            print(t.getPosition())
            return t
        else:
            visited_states.append(t.getPosition())
            print("Visité el estado "+str(t.label)+", pero no es solución")
            print(t.getPosition())
            
            ##########################
            ## Se expande el nodo t ##
            ##########################
            # Se busca la posición de la casilla vacía
            # empty_position[0] es la coordenada x,  empty_position[1] es la coordenada y 
            empty_position=search_empty(t.getPosition()) 
            
            # Se generan todos los estados viables a partir del estado actual que no hayan sido visitados previamente
            # Mover arriba
            if(empty_position[0]>0): # solo se mueve arriba si la posición vacía no está en la primera fila
                new_pos_u=move1(t.getPosition(),empty_position[0],empty_position[1])
                if already_visited(new_pos_u,visited_states)==False:
                    new_state_u=Puzzle8_State(t,label,new_pos_u,level=t.level+1)
                    new_state_u.heuristic_val=heuristic(new_state_u)
                    t.addExpandedState(new_state_u)
                    label=label+1
            
            # Mover a la izquierda
            if(empty_position[1]>0):
                new_pos_l=move2(t.getPosition(),empty_position[0],empty_position[1])
                if already_visited(new_pos_l,visited_states)==False:
                    new_state_l=Puzzle8_State(t,label,new_pos_l,level=t.level+1)
                    new_state_l.heuristic_val=heuristic(new_state_l)
                    t.addExpandedState(new_state_l)
                    label=label+1
            
            # Mover abajo
            if(empty_position[0]<2):
                new_pos_d=move3(t.getPosition(),empty_position[0],empty_position[1])
                if already_visited(new_pos_d,visited_states)==False:
                    new_state_d=Puzzle8_State(t,label,new_pos_d,level=t.level+1)
                    new_state_d.heuristic_val=heuristic(new_state_d)
                    t.addExpandedState(new_state_d)
                    label=label+1
            
            # Mover a la derecha
            if(empty_position[1]<2):
                new_pos_r=move4(t.getPosition(),empty_position[0],empty_position[1])
                if already_visited(new_pos_r,visited_states)==False:
                    new_state_r=Puzzle8_State(t,label,new_pos_r,level=t.level+1)
                    new_state_r.heuristic_val=heuristic(new_state_r)
                    t.addExpandedState(new_state_r)
                    label=label+1
            
            ########################################################
            ## Se agregan los hijos de t a la cola de prioridades ##
            ########################################################
            if t.expanded_states is not None:
                for child in t.expanded_states:
                    h=child.level+child.heuristic_val
                    S.put((h,child))
    return "failure"
