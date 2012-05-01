import lexy
import sys
import thirdpart.swampy.Lumpy as Lumpyy
from time import time 

lumpy = Lumpyy.Lumpy()

t = time()
lumpy.make_reference()

l = lexy.Scanner()
l.load_lexer_definition_from_file('files/lexers/lua.lex')
tk = l.tokenizer(sys.argv[1])

lumpy.object_diagram()
print tk
tf = time()
print '%.2f' %(tf-t)

f = open((sys.argv[1].split('.')[0])+'.token','w')

f.write(tk)
