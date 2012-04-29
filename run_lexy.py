import lexy
import sys

from time import time 

t = time()

l = lexy.Scanner()
tk = l.tokenizer(sys.argv[1])
tf = time()

print '%.2f' %(tf-t)

print tk

f = open((sys.argv[1].split('.')[0])+'.token','w')

f.write(tk)
