#!/usr/bin/env python2
'''
Created on Feb 20, 2012

@author: abara
'''
import sys
import automata as dfa

from time import time 

dfa_file = sys.argv[1]
token_file = sys.argv[2]

lua_automata     = dfa.DeterministicFiniteAutomata(dfa_file).build()
lua_token_source = dfa.TokenSource(token_file)

m = dfa.Manager()

t = time()
r = m.validate( lua_automata , lua_token_source )

tf = time()

print 'Time %.2fs' %(tf-t)
print 'result <',r,'>'