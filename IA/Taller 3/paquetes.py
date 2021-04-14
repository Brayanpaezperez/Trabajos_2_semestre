import numpy
from queue import PriorityQueue

class Puzzle8_State:
    def __init__(self, parent, label, positions=[], move=0):
        self.parent=parent
        self.label=label
        self.solution=numpy.arange(1,10).reshape(3,3)
        self.solution[2][2]=0
        if positions==[]:
            self.positions=numpy.arange(1,10).reshape(3,3)
            self.positions[2][2]=0
        else:
            self.positions=positions
        self.expanded_states=[] # Children
    
    def getPosition(self):  
        return self.positions
    
    def setPosition(self,positions):  
        self.positions=positions
    
    def addExpandedState(self,state):
        self.expanded_states.append(state)
        
    def is_goal(self):
        return numpy.array_equal(self.positions,self.solution)
    
    
#########################################

# Comprobar si dos estados posiciones son iguales
def are_equal_states(position1, position2):
    return numpy.array_equal(position1, position2)
    

# Verificar si un estado ya ha sido visitado (lista de matrices)
def already_visited(state, visited_states):
    for t in visited_states:
        if are_equal_states(state, t):
            return True
    return False

#Buscar la casilla vacía
def search_empty (matrix):
    for i in range (3):
        for j in range (3):
            if matrix[i][j]==0:
                return i,j
    return -1,-1

# Definir las movidas del puzzle de 8 casillas
def move1(position, empty_i, empty_j):
    result=numpy.arange(1,10).reshape(3,3)
    for i in range (3):
        for j in range (3):
            result[i][j] = position[i][j]
    exchange_value=position[empty_i-1][empty_j]
    result[empty_i][empty_j]=exchange_value
    result[empty_i-1][empty_j]=0
    return result

def move2(position, empty_i, empty_j):
    result=numpy.arange(1,10).reshape(3,3)
    for i in range (3):
        for j in range (3):
            result[i][j] = position[i][j]
    exchange_value=position[empty_i][empty_j-1]
    result[empty_i][empty_j]=exchange_value
    result[empty_i][empty_j-1]=0
    return result
    
def move3(position, empty_i, empty_j):
    result=numpy.arange(1,10).reshape(3,3)
    for i in range (3):
        for j in range (3):
            result[i][j] = position[i][j]
    exchange_value=position[empty_i+1][empty_j]
    result[empty_i][empty_j]=exchange_value
    result[empty_i+1][empty_j]=0
    return result

def move4(position, empty_i, empty_j):
    result=numpy.arange(1,10).reshape(3,3)
    for i in range (3):
        for j in range (3):
            result[i][j] = position[i][j]
    exchange_value=position[empty_i][empty_j+1]
    result[empty_i][empty_j]=exchange_value
    result[empty_i][empty_j+1]=0
    return result


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


################# 3er punto ################################
class StateGraph:
    def __init__(self,structure=None,node_content=None):
        if structure is None:
            self.structure={}
        else:
            self.structure=structure
        if node_content is None:
            self.node_content={}
        else:
            self.node_content=node_content

    def getNodes(self):
        keys=list(self.structure.keys())
        node_content={}
        for key in keys:
            node_content[key]=self.node_content[key]
        return node_content
    
    def getNode(self,key):
        return self.node_content[key]
    
    def getEdges(self):
        edges=[]
        for node_key in self.structure.keys():
            for neighbour_node in self.structure[node_key]:
                if [node_key,neighbour_node] not in edges:
                    edges.append([node_key, neighbour_node])
        return edges     
    
    def getEdge(self,key):
        return self.structure[key]
    
######################################################
####### Búsqueda «primero en profundidad» (DFS) ######
######################################################
def Puzzle8_depthfirst(initial_state):
    if initial_state is None:
        return
    visit_queue=[]
    visit_queue.append(initial_state)
    visited_states=[]
    label=1
    while (len(visit_queue)>0):
        t=visit_queue.pop() 
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
            print('\n Metodo: Primero en profundidad \n Pasos a seguir para hallar la solución \n ')
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
                    t.addExpandedState(Puzzle8_State(t,label,new_pos_u))
                    label=label+1
            if(empty_position[1]>0):
                new_pos_l=move2(t.getPosition(),empty_position[0],empty_position[1])
                if(already_visited(new_pos_l,visited_states)==False):
                    visited_states.append(new_pos_l)
                    t.addExpandedState(Puzzle8_State(t,label,new_pos_l))
                    label=label+1
            if(empty_position[0]<2):
                new_pos_d=move3(t.getPosition(),empty_position[0],empty_position[1])
                if(already_visited(new_pos_d,visited_states)==False):
                    visited_states.append(new_pos_d)
                    t.addExpandedState(Puzzle8_State(t,label,new_pos_d))
                    label=label+1
            if(empty_position[1]<2):
                new_pos_r=move4(t.getPosition(),empty_position[0],empty_position[1])
                if(already_visited(new_pos_r,visited_states)==False):
                    visited_states.append(new_pos_r)
                    t.addExpandedState(Puzzle8_State(t,label,new_pos_r))
                    label=label+1
            if t.expanded_states is not None:
                for child in t.expanded_states:
                    visit_queue.append(child)
    return "failure"


def primero_profundidad(pz):
    puzzleBB=Puzzle8_State(None,0,pz.getPosition())
    return Puzzle8_depthfirst(puzzleBB)

#####
def generar_hijos(t,limit):
    global label
    global visited_states
    empty_position=search_empty(t.getPosition())
    if limit == 0:
        return t
    else:
        if(empty_position[0]>0):
            new_pos_u=move1(t.getPosition(),empty_position[0],empty_position[1])
            if already_visited(new_pos_u,visited_states)==False:
                visited_states.append(new_pos_u)                    
                t.addExpandedState(Puzzle8_State(t,label,new_pos_u))
                label=label+1
        if(empty_position[1]>0):
            new_pos_l=move2(t.getPosition(),empty_position[0],empty_position[1])
            if(already_visited(new_pos_l,visited_states)==False):
                visited_states.append(new_pos_l)
                t.addExpandedState(Puzzle8_State(t,label,new_pos_l))
                label=label+1
        if(empty_position[0]<2):
            new_pos_d=move3(t.getPosition(),empty_position[0],empty_position[1])
            if(already_visited(new_pos_d,visited_states)==False):
                visited_states.append(new_pos_d)
                t.addExpandedState(Puzzle8_State(t,label,new_pos_d))
                label=label+1
        if(empty_position[1]<2):
            new_pos_r=move4(t.getPosition(),empty_position[0],empty_position[1])
            if(already_visited(new_pos_r,visited_states)==False):
                visited_states.append(new_pos_r)
                t.addExpandedState(Puzzle8_State(t,label,new_pos_r))
                label=label+1
        return t
#############################################
## Búsqueda en profundidad limitada (DLS). ## 
#############################################

def Puzzle8_depthfirst_limit(initial_state,limit):
    global end_recursion
    global visited_states
    global label
    global lt1
    if end_recursion == True:
        return "success"
    elif initial_state is None:
        return 'fallo'
    elif limit == 0:
        return "error_corte"   
    t=initial_state
    if len(visited_states)==0:
        visited_states.append(initial_state.getPosition())
    
    if t.is_goal() == True:
        print("\nEl estado solución es: "+str(t.label))
        print(t.getPosition())
        end_recursion = True
        return "success"
    else:
        print("Evaluamos el estado "+str(t.label)+", pero no es solución",' Profundidad:  ',lt1-limit)
        print(t.getPosition())
        ocurrio_corte=False
        t=generar_hijos(t,limit-1)
        if (t.expanded_states is not None):
            for child in t.expanded_states:
                result=Puzzle8_depthfirst_limit(child,limit-1)
                if result == "fallo":
                    print("Se termina esta rama con error: " + result)     
                    return result
                elif result == "error_corte":
                    ocurrio_corte=True
            if ocurrio_corte:
                return "error_corte"
        if end_recursion:
            return "success"
            
        else:
            return "seguir"
    
            
def profundidad_limitada(pz,lt):
    global visited_states
    global end_recursion
    global label
    global lt1
    lt1=lt
    visited_states=[]
    end_recursion=False
    label=1
    puzzleBB=Puzzle8_State(None,0,pz.getPosition())
    
    return Puzzle8_depthfirst_limit(puzzleBB,lt)  


###################################################
#####  Búsqueda en profundidad iterada ID-DLS #####
###################################################

def Puzzle8_depthfirst_limit_i(initial_state,limit):
    global end_recursion
    global visited_states
    global label
    if end_recursion == True:
        return "success"
    elif initial_state is None:
        return 'fallo'
    elif limit == 0:
        return "error_corte"   
    t=initial_state
    if len(visited_states)==0:
        visited_states.append(initial_state.getPosition())
    
    if t.is_goal() == True:
        print("\nEl estado solución es: "+str(t.label))
        print(t.getPosition())
        end_recursion = True
        return "success"
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
                    return result
                elif result == "error_corte":
                    ocurrio_corte=True
            if ocurrio_corte:
                return "error_corte"
        if end_recursion:
            return "success"
        else:
            return "seguir"
            
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
        result=Puzzle8_depthfirst_limit_2(t,limit_level+1)
        print("El resultado para esta iteración ",limit_level,' es :',result)
        if result=="fallo": 
            print("No se pudo encontrar una respuesta")
            return "fallo"
        elif result=="success":
            return 
        
    if result=="error_corte":
        print("No se pudo encontrar una respuesta hasta el nivel ", max_level)
        result="fallo_corte"
    return   
        
    
#########################
## Búsqueda en anchura ##
#########################

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
            print('\n Metodo: Busqueda en Anchuro \n Pasos a seguir para hallar la solución \n ')
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
                    t.addExpandedState(Puzzle8_State(t,label,new_pos_u))
                    label=label+1
            if(empty_position[1]>0):
                new_pos_l=move2(t.getPosition(),empty_position[0],empty_position[1])
                if(already_visited(new_pos_l,visited_states)==False):
                    visited_states.append(new_pos_l)
                    t.addExpandedState(Puzzle8_State(t,label,new_pos_l))
                    label=label+1
            if(empty_position[0]<2):
                new_pos_d=move3(t.getPosition(),empty_position[0],empty_position[1])
                if(already_visited(new_pos_d,visited_states)==False):
                    visited_states.append(new_pos_d)
                    t.addExpandedState(Puzzle8_State(t,label,new_pos_d))
                    label=label+1
            if(empty_position[1]<2):
                new_pos_r=move4(t.getPosition(),empty_position[0],empty_position[1])
                if(already_visited(new_pos_r,visited_states)==False):
                    visited_states.append(new_pos_r)
                    t.addExpandedState(Puzzle8_State(t,label,new_pos_r))
                    label=label+1
            if t.expanded_states is not None:
                for child in t.expanded_states:
                    visit_queue.append(child)
    return "failure"


def primero_anchura(pz):
    puzzleBB=Puzzle8_State(None,0,pz.getPosition())
    return Puzzle8_breadthfirst(puzzleBB)

###############
#### GRAFO ####
###############

class StateGraph:
    def __init__(self,structure=None,node_content=None):
        if structure is None:
            self.structure={}
        else:
            self.structure=structure
        if node_content is None:
            self.node_content={}
        else:
            self.node_content=node_content

    def getNodes(self):
        keys=list(self.structure.keys())
        node_content={}
        for key in keys:
            node_content[key]=self.node_content[key]
        return node_content
    
    def getNode(self,key):
        return self.node_content[key]
    
    def getEdges(self):
        edges=[]
        for node_key in self.structure.keys():
            for neighbour_node in self.structure[node_key]:
                if [node_key,neighbour_node] not in edges:
                    edges.append([node_key, neighbour_node])
        return edges     
    
    def getEdge(self,key):
        return self.structure[key]



###################################################
## Búsqueda de costo uniforme  (función externa) ##
###################################################



def UniformCostSearch (graph, root_label,end_label):
    lista_d=[]
    lista_r=[]
    print ("Nodo de partida:",root_label)
    print ("Nodo de llegada:",end_label)
    for n in graph.getNodes():
        graph.node_content[n]=(0,False)
    graph.node_content[end_label]=(0,True)
    if graph.getNodes() is None:
        return False
    else:
        node=graph.getNode(root_label)
        if node is None:
            return False
    
    visited_nodes=set()
    pq=PriorityQueue() #La estructura de datos principal, para priorizar los recorridos de menor coste
    pq.put((node[0],root_label,node[1])) # Se crea una cola de prioridad ad hoc con tuplas: (0: costo, 1: etiqueta_estado, 2: es_exito)
    
    iteration=0
    iterate=True
    while iterate:
        if pq.empty():
            return_value="Error"
            iterate=False
            #break #sale del bucle de evaluación
        
        t=pq.get() # En el primer paso, es el nodo raíz, luego será la tupla con menor costo
#         print ("\nNodo actual:", t[1], "-Lista de nodos visitados:",visited_nodes)
        

        if t[2] == True: # prueba de éxito
#             print ("Estado objetivo encontrado")
            return_value=t
            iterate=False
            
            
        else:
            visited_nodes.add(t[1]) # si la tupla t no corresponde al estado solución (llegada) se agrega la etiqueta "t[1]" a la lista de visitados
           
            for neighbour in graph.getEdge(t[1]): # el vecino tiene la misma estructura de un nodo del grafo (entrada de diccionario), se toma el nodo con clave "t[1]"
                if neighbour[0] not in visited_nodes: # Se revisa que la etiqueta del nodo vecino no esté en la lista de visitados
                    neighbour_cost=t[0]+neighbour[1]
                    pq.put((neighbour_cost,neighbour[0],graph.getNodes()[neighbour[0]][1]))
                    lista_d.append(neighbour_cost)
                    lista_r.append(list(visited_nodes))
#                     print ("-Iteración: ",iteration)
#                     print ("-Origen: ",t[1],"-Visito:",neighbour[0], "-Costo:", neighbour_cost,"-¿Es solución? ",graph.getNode(neighbour[0])[1])
                                        
#             print('\n')
            iteration=iteration+1
#     lista_r.append(end_label)
    
    print('Costo de: ',return_value[0],'\nCiudades visitadas antes de llegar al objetivo final:', lista_r[lista_d.index(return_value[0])])
    return return_value
 