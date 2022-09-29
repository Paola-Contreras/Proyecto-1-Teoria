import json
import sys

from postfix import regex_to_postfix
class charType:
    EPSILON = 0
    SYMBOL = 1
    CONCAT = 2
    UNION  = 3
    KLEENE = 4
followpostable = []
followpostable.append([[],[]])
simbolsfound = []
class ExpressionTree:

    def __init__(self, charType, value=None,number = None, nulable = False):
        self.charType = charType
        self.value = value
        self.left = None
        self.right = None
        self.number = number
        self.nulable = nulable
        self.primeraP = []
        self.ultimaP = []

    def nulablre(self):
        if self.charType == charType.SYMBOL:
            return False
        elif self.charType == charType.CONCAT:
            return self.left.nulablre() and self.right.nulablre()
        elif self.charType == charType.UNION:
            return self.left.nulablre() or self.right.nulablre()
        elif self.charType == charType.KLEENE:
            return True
        elif self.charType == charType.EPSILON:
            return True
    
    def firstpos(self):
        if self.charType == charType.SYMBOL:
            return [self.number]
        elif self.charType == charType.CONCAT:
            if self.left.nulablre():
                return self.left.firstpos() + self.right.firstpos()
            else:
                return self.left.firstpos()
        elif self.charType == charType.UNION:
            return self.left.firstpos() + self.right.firstpos()
        elif self.charType == charType.KLEENE:
            return self.left.firstpos()
        elif self.charType == charType.EPSILON:
            return []
    
    def lastpos(self):
        if self.charType == charType.SYMBOL:
            return [self.number]
        elif self.charType == charType.CONCAT:
            if self.right.nulablre():
                return self.left.lastpos() + self.right.lastpos()
            else:
                return self.right.lastpos()
        elif self.charType == charType.UNION:
            return self.left.lastpos() + self.right.lastpos()
        elif self.charType == charType.KLEENE:
            return self.left.lastpos()
        elif self.charType == charType.EPSILON:
            return []
     

def make_exp_tree(regexp):
    num = 1
    stack = []
    for c in regexp:
        if c == "+":
            z = ExpressionTree(charType.UNION,c)
            z.right = stack.pop()
            z.left = stack.pop()
            z.nulable = z.nulablre()
            z.primeraP = z.firstpos()
            z.ultimaP = z.lastpos()
            stack.append(z)
        elif c == ".":
            z = ExpressionTree(charType.CONCAT,c)
            z.right = stack.pop()
            z.left = stack.pop()
            z.nulable = z.nulablre()
            z.primeraP = z.firstpos()
            z.ultimaP = z.lastpos()
            stack.append(z)
        elif c == "*":
            z = ExpressionTree(charType.KLEENE,c)
            z.left = stack.pop() 
            z.nulable = z.nulablre()
            z.primeraP = z.firstpos()
            z.ultimaP = z.lastpos()
            stack.append(z)
        elif c == "(" or c == ")":
            continue  
        elif c == "\u03b5":
            z = ExpressionTree(charType.EPSILON, c,None,True)
            z.primeraP = []
            z.ultimaP = []
            stack.append(z)
        else:
            z = ExpressionTree(charType.SYMBOL, c,num, False)
            z.primeraP = z.firstpos()
            z.ultimaP = z.lastpos()
            stack.append(z)
            followpostable.append([[],[c],z])
            c in simbolsfound or (c != '#' and simbolsfound.append(c))
            num = num + 1
    return stack[0]

def Followpos(node):
    if node.charType == charType.SYMBOL:
        #followpostable.append([])
        pass
    elif node.charType == charType.CONCAT:
        Followpos(node.left)
        Followpos(node.right)
        for i in node.left.ultimaP:
            
            followpostable[i][0]= followpostable[i][0] + node.right.primeraP
    elif node.charType == charType.UNION:
        Followpos(node.left)
        Followpos(node.right)
    elif node.charType == charType.KLEENE:
        Followpos(node.left)
        for i in node.left.ultimaP:

            followpostable[i][0]= followpostable[i][0] + node.left.primeraP


def arrange_afd(states,transitionTable,followpostable):
    afd = {}
    afd['states'] = []
    afd['letters'] = simbolsfound
    afd['transition_function'] = []
    afd['start_states'] = ["Q1"]
    afd['final_states'] = []

    for i in states:
        afd['states'].append("Q"+str(states.index(i)+1))

    for i in transitionTable:
        afd['transition_function'].append(("Q"+str(states.index(i[0])+1), i[1], "Q"+str(states.index(i[2])+1)))
    
    lasti = len(followpostable)-1

    for i in states:
        if lasti in i:
            afd['final_states'].append("Q"+str(states.index(i)+1))

    return afd
        
def out_afd(afd):
    with open('output_directo.json', 'w') as outjson:
        outjson.write(json.dumps(afd, indent = 4))


def generate_afdD(regex):
    aumentada = regex + '.#'
    postfix = regex_to_postfix(aumentada)
    tree = make_exp_tree(postfix)
    Followpos(tree)
    transitionTable = []
    stack = []
    states = []
    s0 = followpostable[1][0]
    stack.append(s0)
    states.append(s0)

    while len(stack) > 0:
        s = stack.pop()
        for c in simbolsfound:
            u = []
            for i in s:
                if c in followpostable[i][1]:
                    for k in followpostable[i][0]:
                        if k not in u:
                            u.append(k)
                    #u = u + followpostable[i][0]
            if len(u) > 0:
                if u not in states:
                    states.append(u)
                    stack.append(u)
                transitionTable.append([s,c,u])
            else:
                transitionTable.append([s,c,[]])

    states.append([])
    solve = arrange_afd(states,transitionTable,followpostable)

    out_afd(solve)

    return solve

