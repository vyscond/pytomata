import lexy
import sys

from time import time 

t = time()

l = lexy.Scanner()
l.load_lexer_definition_from_file('files/lexers/java.lex')
tk = l.tokenizer(sys.argv[1])

print tk
tf = time()
print '%.2f' %(tf-t)

f = open((sys.argv[1].split('.')[0])+'.token','w')

f.write(tk)
