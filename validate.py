import lexy
import automata

import sys

from time import time 

t = time()

#----------------------------------------------------------

fullpath = sys.argv[1]

directory_qtt = fullpath.count('/')

path_without_filename = ''

fullfilename = ''

slash = 0

for c in sys.argv[1]:

    if slash == directory_qtt:

        fullfilename += c

    else :

        path_without_filename += c

    if c == '/':

        slash += 1
    
extension = fullfilename.split('.')[1]

filename = fullfilename.split('.')[0]

print '+--------------------------------+'

print fullpath

print path_without_filename

print fullfilename

print filename

print extension


print '+--------------------------------+'
print '|    --- generating token ---    |'
print '+--------------------------------+'

print 'tokenizing -> '+fullpath

tokenlist = lexy.Scanner().tokenizer(fullpath)
#tokenlist = tokenlist[0: (len(tokenlist) - 1) ]

#--- misc
print '+---------- Text ----------+'
for line in tokenlist.split('\n'):
	
	print '| ~ '+line
print '+--------------------------+'

print 'token list saved as -> ' + (path_without_filename+filename+'.token')

f = open( (path_without_filename+filename+'.token') , 'w' )
f.write(tokenlist)
f.close()

print '+--------------------------------+'
print '|         --- parsing ---        |'
print '+--------------------------------+'

#--- loading dfa

parser_path = 'files/parsers/'
print 'loading dfa for language -> ' + extension + '[' + parser_path + extension + '.dfa]'
parser_fullpath = parser_path + extension + '.dfa'

dfa = automata.DeterministicFiniteAutomata( parser_fullpath ).build()

#--- loading the token list

print 'loading token list -> ' + path_without_filename + filename + '.token'
tokenlist_path = path_without_filename + filename + '.token'

s = open(tokenlist_path)

token_source = automata.TokenSource( tokenlist_path )

m  = automata.Manager()
answer = m.validate( dfa, token_source )

print '<',answer,'>'

#----------------------------------------------------------

tf = time()

print 'Time %.2fs' %(tf-t)
