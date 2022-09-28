
import json
import sys

non_symbols = ['+', '*', '.', '(', ')']
afn = {}

class charType:
    SYMBOL = 1
    CONCAT = 2
    UNION  = 3
    KLEENE = 4


class afnState:
    def __init__(self):
        self.next_state = {}


class ExpressionTree:

    def __init__(self, charType, value=None):
        self.charType = charType
        self.value = value
        self.left = None
        self.right = None

    

def make_exp_tree(regexp):
    stack = []
    for c in regexp:
        if c == "+":
            z = ExpressionTree(charType.UNION,c)
            z.right = stack.pop()
            z.left = stack.pop()
            stack.append(z)
        elif c == ".":
            z = ExpressionTree(charType.CONCAT,c)
            z.right = stack.pop()
            z.left = stack.pop()
            stack.append(z)
        elif c == "*":
            z = ExpressionTree(charType.KLEENE,c)
            z.left = stack.pop() 
            stack.append(z)
        elif c == "(" or c == ")":
            continue  
        else:
            stack.append(ExpressionTree(charType.SYMBOL, c))
    return stack[0]



def compute_regex(exp_t):
    # returns E-afn
    if exp_t.charType == charType.CONCAT:
        return do_concat(exp_t)
    elif exp_t.charType == charType.UNION:
        return do_union(exp_t)
    elif exp_t.charType == charType.KLEENE:
        return do_kleene_star(exp_t)
    else:
        return eval_symbol(exp_t)


def eval_symbol(exp_t):
    start = afnState()
    end = afnState()
    
    start.next_state[exp_t.value] = [end]
    return start, end


def do_concat(exp_t):
    left_afn  = compute_regex(exp_t.left)
    right_afn = compute_regex(exp_t.right)

    left_afn[1].next_state['ε'] = [right_afn[0]]
    #right_afn[0]=left_afn[1]
    return left_afn[0], right_afn[1]


def do_union(exp_t):
    start = afnState()
    end = afnState()

    first_afn = compute_regex(exp_t.left)
    second_afn = compute_regex(exp_t.right)

    start.next_state['ε'] = [first_afn[0], second_afn[0]]
    first_afn[1].next_state['ε'] = [end]
    second_afn[1].next_state['ε'] = [end]

    return start, end


def do_kleene_star(exp_t):
    start = afnState()
    end = afnState()

    starred_afn = compute_regex(exp_t.left)

    start.next_state['ε'] = [starred_afn[0], end]
    starred_afn[1].next_state['ε'] = [starred_afn[0], end]

    return start, end


def arrange_transitions(state, states_done, symbol_table):
    global afn

    if state in states_done:
        return

    states_done.append(state)

    for symbol in list(state.next_state):
        if symbol not in afn['letters'] and symbol != 'ε':
            afn['letters'].append(symbol)
        for ns in state.next_state[symbol]:
            if ns not in symbol_table:
                symbol_table[ns] = sorted(symbol_table.values())[-1] + 1
                q_state = "Q" + str(symbol_table[ns])
                afn['states'].append(q_state)
            afn['transition_function'].append(["Q" + str(symbol_table[state]), symbol, "Q" + str(symbol_table[ns])])

        for ns in state.next_state[symbol]:
            arrange_transitions(ns, states_done, symbol_table)

def final_st_afn():
    global afn
    for st in afn["states"]:
        count = 0
        for val in afn['transition_function']:
            if val[0] == st and val[2] != st:
                count += 1
        if count == 0 and st not in afn["final_states"]:
            afn["final_states"].append(st)


def arrange_afn(fa):
    global afn
    afn['states'] = []
    afn['letters'] = []
    afn['transition_function'] = []
    afn['start_states'] = []
    afn['final_states'] = []
    q_1 = "Q" + str(1)
    afn['states'].append(q_1)
    arrange_transitions(fa[0], [], {fa[0] : 1})
    afn["start_states"].append("Q1")
    final_st_afn()



def output_afn():
    global afn
    with open('output_AFN.json', 'w') as outjson:
        outjson.write(json.dumps(afn, indent = 4))

def generate_afn(pr):
    et = make_exp_tree(pr)
    fa = compute_regex(et)
    arrange_afn(fa)
    output_afn()
    return afn