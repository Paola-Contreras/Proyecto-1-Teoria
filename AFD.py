#Convert a AFN to a AFD 
import json

#Function to get tha AFN generate by using the thompson algorithm 
def openJson():
    with open('output_AFN.json', 'r') as json_file:
	    return json.load(json_file)
    
#Function to get the Closures of each state 
def eClosures(state):
    temp =[]
    closures = []
    for i in state:
        # conditional to see if the state is already on temp to make sure we dont repet a state on the closure
        if i not in temp:
            #Saves the first state for the closure and use these to get all the posible closures
            temp.append(i)  
            closures.append(i)

    while len(temp) != 0:
        states =  temp.pop()
        # cycle use to get only the data of transition_function
        for j in afn['transition_function']:
            # Get each value of the list get on the cycle for 
            first = j[0]
            second = j[1]
            third = j[2]
            #Get all the transitions ε with the satate 
            if second == 'ε' and  first == states:
                #conditional to see if the state is already saved
                if third not in closures:
                    temp.append(third) 
                    closures.append(third)

    return closures

#Function to convert the AFN to AFD
def convertToAFD(file):
    afd ={}

    temp1 =['Q1'] 
    states =[['Q1']] 
    subset = []
    transition = []
    finalStates = []

    #Variables that contein data of the given Json 
    alphabet = file ['letters']
    final_state = file['final_states']
    transitions = file ['transition_function']

    while len(temp1) != 0:
        #removes state of list and is used to evaluate
        temp_state = temp1.pop()

        #Cycle to get each value of the alphabet
        for i in alphabet:
            #Cehck if the state is not the start state 
            if temp_state != 'Q1':
                n_states = temp_state
            #If we get the start state  we convert these to a list, to keep track of the new transitions 
            else: 
                n_states = [temp_state]
            
            #Calculate closures 
            closure = eClosures(n_states)
    
            #Cycle to get each transitions of AFN
            for j in transitions:
                #Values of the list
                first = j[0]
                second = j[1]
                third = j[2]
                #Cycle to get each value of the closure list 
                for k in closure :
                    #Condditional that checks the state and the value of move
                    if first == k and second == i:
                        #If the value is not ε these is append the state to n_states
                        if third not in n_states:
                            n_states.append(third)
           
            subset = eClosures(n_states)

            if len(subset) != 0:
                # Conditional that checks if the set is already on states 
                if subset not in states:
                    if subset not in temp1:
                        # Saves the set on the states list and use is as a new state by appending it on temp
                        states.append(subset)
                        temp1.append(subset)

                #Conditional that keeps track of every transition acording to the alphabet 
                # if temp_state != 'Q1':
                #     transition.append((temp_state, i, subset))
                # else:
                #     transition.append((temp_state, i, subset))

                if temp_state == 'Q1':
                    transition.append(("Q"+str(states.index([temp_state])+1), i, "Q"+str(states.index(subset)+1)))
                else:
                    
                    transition.append(("Q"+str(states.index(temp_state)+1), i, "Q"+str(states.index(subset)+1)))
            

    #Convert final state of AFN to string 
    final_state = ' '.join ([str(item) for item in file['final_states']])

    #Cycle to get each states of the AFD 
    for i in states:
        #Check on each new state conteins the final state of the AFN on it 
        if final_state in i:
            #Save the list that conteins the final state on another list 
            finalStates.append(i)
    
    #Generate AFD 
    afd['alphabet'] = alphabet
    afd['start_state'] = file['start_states']
    afd['states'] = states 
    afd['final_states'] = finalStates
    afd['transition'] = transition

    return  afd 

#Function to generate file with the AFD
def GenerateJson(afd):
    with open('AFD.json', 'w') as file:
        json.dump(afd, file, indent=4)

def generate_afd():
    global afn
    afn = openJson()
    afd = convertToAFD(afn)
    GenerateJson(afd)
    return afd

# print('----------- AFN -----------','\n',afn)
# print('----------- AFD -----------','\n',afd)

#Show AFD
#Color Palet
