#!/usr/bin/env python2
'''
Created on Feb 20, 2012

@author: abara
'''

import automata as dfa

print '\n+---------------------------+\n'
print '        Loading/Build DFA        '
print '\n+---------------------------+\n'


print '\n'

dfa_lua = dfa.DeterministicFiniteAutomata('files/lua_test/lua_func.dfa').build()

print '\n+---------------------------+\n'
print '        Build DFA Manager        '
print '\n+---------------------------+\n'

m = dfa.Manager()

print '\n+---------------------------+\n'
print '        Load DFA for test        '
print '\n+---------------------------+\n'

m.add_dfa(dfa_lua)

print '\n+---------------------------+\n'
print '        Load source file         '
print '\n+---------------------------+\n'

source_file = dfa.Source('files/lua_test/hello.lua')

print source_file.original_text

m.set_source ( source_file )

print '\n+---------------------------+\n'
print '        Run validate test        '
print '\n+---------------------------+\n'

r = m.validate( m.get_dfa( dfa_lua.get_name() ) )
