# -*- coding: iso-8859-1 -*


# tipos pre-definidos

# alpha_numeric
# alphabetic
# integer_number
# float_point_number

# char e stringdevem ser definidos pelo usuario
# pois assim como no python, e outras linguagens de ducktype
# nada é realmente primitivo! então a definição de char e string é 
# diferente de tipagens em C e Java

class Scanner(object):

    def __init__(self):

        self.symbol_table = {}
        
        self.tokens = []
        

    def run(self, file_path):

        text = (''.join(open(file_path)))
        
        # daqui pra frente é reconhecer na força bruta né!? ;D core, core, core!!! seu estupido
        
        LAST_CHAR_READED = ''
        
        BUFFER = ''



