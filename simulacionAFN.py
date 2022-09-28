import numpy as np
import pandas as pd

CEND = '\33[0m'
CRED = '\33[91m'
CYELLOW = '\33[93m'
CGREEM = '\33[92m'
CBLUE = '\33[94m'

def e_clouser(states):
    #global afn
    stack = []
    res = []
    for state in states:
        if state not in stack:
            stack.append(state)
            res.append(state)
        
    while len(stack) > 0:
        state = stack.pop()
        for i in afn['transition_function']:
            if i[0] == state and i[1] == 'ε':
                if i[2] not in res:
                    res.append(i[2])
                    stack.append(i[2])
    return res



def transition(q, a, tabla):
    qq = []
    for s in q :
       x = tabla[(tabla['q'] == s) & (tabla['a'] == a)]['d(q,a)']
       if(len(x) > 0):
           qq.append(x.values[0])
    return e_clouser(qq)
    #x = tabla[(tabla['q'] == q) & (tabla['a'] == a)]['d(q,a)']
    #return x.values[0]


def final_state(q, w, tabla):
    n = len(w)
    if (n == 0):
        return e_clouser(q)
    else:
        a = (w[0])
        qq = transition(e_clouser(q), a, tabla)
        x = final_state(qq, w[1:], tabla)
        return x


def accepted(q, w, F, tab):
    x = final_state(q, w, tab)

    for i in x:
        if i in F:
            return print(CEND,'\nThe word',CGREEM,w,CEND,'is accepted\n\n')
    return print(CEND,'\nThe word',CRED,w,CEND,'is NOT accepted\n\n')
    # if (x in F):
    #     return print(CEND,'\nThe word',CGREEM,w,CEND,'is accepted\n\n')
    # else:
    #     return print(CEND,'\nThe word',CRED,w,CEND,'is NOT accepted\n\n')

def derivation(q, w, tabla):
    n = len(w)
    if (n == 0):
        return print('\33[92m({},{})\33[93m => \33[94m{}'.format(q,'',q))
    else: 
        a = (w[0])
        q = e_clouser(q)
        qq = transition(q, a, tabla)
        x = derivation(qq, w[1:],tabla)
        return print('\33[92m({},{})\33[93m => \33[94m({},{})'.format(q,w,qq,w[1:]))


def simularAFN(w,afn_r):
    global afn
    global table 
    afn = afn_r
    
    
    
    table = np.array(afn['transition_function'])
    tab = pd.DataFrame(data=table, columns=['q', 'a', 'd(q,a)'])
    #print(table)
    
    derivation(['Q1'], w, tab)
    accepted(['Q1'], w,afn['final_states'], tab)
