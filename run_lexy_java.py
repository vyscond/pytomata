import lexy2 as lexy
import sys

from time import time 

t = time()

l = lexy.Scanner('files/lexers/java.lex')

exit(0)

tk = l.tokenizer(sys.argv[1])

print tk
tf = time()
print '%.2f' %(tf-t)

f = open((sys.argv[1].split('.')[0])+'.token','w')

f.write(tk)
