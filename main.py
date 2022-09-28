
from postfix import regex_to_postfix
from AFN import generate_afn
from AFD import generate_afd
from AFDirecto import generate_afdD
from Minimizacion import minimise
from simulacionAFD import simular
from simulacionAFN import simularAFN


CEND = '\33[0m'
CRED = '\33[91m'
CYELLOW = '\33[93m'
CGREEM = '\33[92m'
CBLUE = '\33[94m'

reg = "(b+a)*c"
postfix = regex_to_postfix(reg)
print('\33[93mPOSTFIX: ',postfix,'\33[94m')

print(CRED,'\n\n-----------------',CEND,CYELLOW,'AFN',CEND,CRED,' -------------------')
afn = generate_afn(postfix)
print('Estado inicial: ',CGREEM,afn['start_states'],CRED)
print('Estado de aceptacion: ',CGREEM,afn['final_states'],CRED)
print('Estados: ',CGREEM,afn['states'],CRED)
print('Alfabeto: ',CGREEM,afn['letters'],CRED)
print('Transiciones: ')
for inicial, simbolo, final in afn['transition_function']:
    print(CGREEM,inicial,CYELLOW,'==',CBLUE,F"({simbolo})",CYELLOW,'==>',CGREEM,final,CRED)
    #print(f"{inicial:4} == ({simbolo}) ==> {final:4}")
print('\033[0m')


print(CRED,'\n\n-----------------',CEND,CYELLOW,'AFD',CEND,CRED,' -------------------\n')
afd = generate_afd()
print(CRED,'\n\n-------------------',CEND,CYELLOW,'AFD',CEND,CRED,'-------------------\n')
print ('Alfabeto: ', CGREEM, afd['alphabet'], CRED )
print ('Estado inicial: ', CGREEM, afd['start_stateB'], CRED )
print ('Estados de aceptación: ', CGREEM, afd['final_statesB'], CRED )
print ('Estados: ', CGREEM, afd['statesB'], CRED )
print ('Transiciones: ')
for inicial, simbolo,final in afd['transitionB']:
    print(CGREEM, inicial, CYELLOW, '==', CBLUE, F"({simbolo})",CYELLOW, '==>',CGREEM,final,CRED)

print(CRED,'\n\n-----------------',CEND,CYELLOW,'AFD Directo',CEND,CRED,' -------------------\n')
afdD = generate_afdD(reg)
print('Estado inicial: ',CGREEM,afdD['start_states'],CRED)
print('Estado de aceptacion: ',CGREEM,afdD['final_states'],CRED)
print('Estados: ',CGREEM,afdD['states'],CRED)
print('Alfabeto: ',CGREEM,afdD['letters'],CRED)
print('Transiciones: ')
for inicial, simbolo, final in afdD['transition_function']:
    print(CGREEM,inicial,CYELLOW,'==',CBLUE,F"({simbolo})",CYELLOW,'==>',CGREEM,final,CRED)


print(CRED,'\n\n-----------', CYELLOW,'Simulacion AFN',CRED ,'-----------\n')
simularAFN('bbabaabbab',afn)
simularAFN('bbac',afn)

print(CRED,'\n\n-----------', CYELLOW,'Simulacion AFD',CRED ,'-----------')
simular('bbabaabbab',afdD['transition_function'],afdD['final_states'])
simular('bbac',afdD['transition_function'],afdD['final_states'])

print(CRED,'\n\n-----------', CYELLOW,'Minimizacion AFD',CRED ,'-----------')
afd_min = minimise()
#afd_min = afdD
print('Estado inicial: ',CGREEM,afd_min['start_state'],CRED)
print('Estado de aceptacion: ',CGREEM,afd_min['final_states'],CRED)
print('Estados: ',CGREEM,afd_min['states'],CRED)
print('Alfabeto: ',CGREEM,afd_min['letters'],CRED)
print('Transiciones: ')
#print(afd_min['transition_function'])
for inicial, simbolo, final in afd_min['transition']:
    print(CGREEM,inicial,CYELLOW,'==',CBLUE,F"({simbolo})",CYELLOW,'==>',CGREEM,final,CRED)


