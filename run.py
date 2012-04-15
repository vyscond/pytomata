#!/usr/bin/env python2
'''
Created on Feb 20, 2012

@author: abara
'''

import automata as dfa

dfa_test = dfa.DeterministicFiniteAutomata('files/simplelua.dfa').build()

print '\n+---------------------------+\n'

m = dfa.Manager()

m.add_dfa(dfa_test)

m.set_source ( dfa.Source('files/hello.lua') )

r = m.validate( m.get_dfa( dfa_test.get_name() ) )

print 'Result >> ', 

print r

