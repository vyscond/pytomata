# -*- coding: iso-8859-1 -*


# tipos pre-definidos

# alpha_numeric
# alphabetic
# integer_number
# float_point_number

# char e stringdevem ser definidos pelo usuario
# pois assim como no python, e outras linguagens de ducktype
# nada � realmente primitivo! ent�o a defini��o de char e string � 
# diferente de tipagens em C e Java

class Scanner(object):

    def __init__(self):

        self.symbol_table = {}
        
        self.tokens = []
        

    def run(self, file_path):

        text = (''.join(open(file_path)))
        
        # daqui pra frente � reconhecer na for�a bruta n�!? ;D core, core, core!!! seu estupido
        
        LAST_CHAR_READED = ''
        
        BUFFER = ''



