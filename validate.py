import lexy
import automata

import sys

from time import time 

t = time()

#----------------------------------------------------------

directory_qtt = sys.argv[1].count('/')

print directory_qtt

path = ''

fullfilename = ''

slash = 0

for c in sys.argv[1]:

    if slash == directory_qtt:

        fullfilename += c

    else :

        path += c

    if c == '/':

        slash += 1
    
extension = fullfilename.split('.')[1]

filename = fullfilename.split('.')[0]

print path
print filename
print extension

print 'generating token'

tokenized_source = lexy.Scanner().tokenizer(path+fullfilename)

f = open( path+filename+'.token' , 'w' )

f.write(tokenized_source)

print 'parsing'

dfa          = automata.DeterministicFiniteAutomata( 'files/parsers/'+extension+'.dfa' ).build()
token_source = automata.TokenSource( path+filename+'.token' )

answer = automata.Manager().validate( dfa, token_source )

print '<',answer,'>'

#----------------------------------------------------------

tf = time()

print 'Time %.2fs' %(tf-t)