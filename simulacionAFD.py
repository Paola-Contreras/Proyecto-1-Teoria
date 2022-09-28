import numpy as np
import pandas as pd

CEND = '\33[0m'
CRED = '\33[91m'
CYELLOW = '\33[93m'
CGREEM = '\33[92m'
CBLUE = '\33[94m'



def transition(q, a, tabla):
    x = tabla[(tabla['q'] == q) & (tabla['a'] == a)]['d(q,a)']
    return x.values[0]


def final_state(q, w, tabla):
    n = len(w)
    if (n == 0):
        return q
    else:
        a = (w[0])
        qq = transition(q, a, tabla)
        x = final_state(qq, w[1:], tabla)
        return x


def accepted(q, w, F, tab):
    x = final_state(q, w, tab)
    if (x in F):
        return print(CEND,'\nThe word',CGREEM,w,CEND,'is accepted\n\n')
    else:
        return print(CEND,'\nThe word',CRED,w,CEND,'is NOT accepted\n\n')

def derivation(q, w, tabla):
    n = len(w)
    if (n == 0):
        return print('\33[92m({},{})\33[93m => \33[94m{}'.format(q,'',q))
    else: 
        a = (w[0])
        qq = transition(q, a, tabla)
        x = derivation(qq, w[1:],tabla)
        return print('\33[92m({},{})\33[93m => \33[94m({},{})'.format(q,w,qq,w[1:]))

def simular(w, transacciones,acept):
    global table 
    table = np.array(transacciones)
    #print(table)

    tab = pd.DataFrame(data=table, columns=['q', 'a', 'd(q,a)'])
    #print(tab)

    #final_state('Q1', w, tab)

    derivation('Q1', w, tab)
    accepted('Q1', w,acept, tab)
