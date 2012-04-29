# -*- coding: iso-8859-1 -*

'''
Created on Feb 20, 2012

@author: abara
'''
import util.ascii_art as Ascii

class State(object):

    def set_initial(self, bool):
        
        self.initial = bool
    
    def is_initial(self, bool):
        
        return self.initial
    
    def set_final(self, bool):
        
        self.final = bool
        
    def is_final(self):
    
        return self.final

    def __init__(self, state_name):
        
        self.final = False
        
        self.initial = False
        
        self.state_name = state_name
        
        self.transition_states = {}
        
    def get_name(self):
        
        return self.state_name
        
    def add_production_rule(self, consume_symbol, state):
        
        self.transition_states[consume_symbol] = state
        
    def get_next_state(self, consume_symbol):
        
        return self.transition_states.get(consume_symbol)

#-------------------------------------------------------------------------------

class DeterministicFiniteAutomata(object):
    
    def get_name(self):
        
        return self.name
    
    def __init__(self, dfa_file_path):
        
        self.name = ''
        
        self.state_list = []
        
        self.initial_state = [] # the "root node"
        
        self.final_state_list = []

        self.production_rules = []
        
        self.alphabet_list = []
        
        self.root = None # vai ser o no inicial
        
        #--- filtrando o nome do DFA baseado no label usado no arquivo
        
        self.name = dfa_file_path.split('/')[-1].replace('.dfa','')
        
        
        #--- transformando o objeto do tipo [file] em [string]

        self.dfa_definition = ''.join(open(dfa_file_path))
        
        #----------------------------------------------------------
        #
        #                     filling structs
        #
        #----------------------------------------------------------

        #--- a função [search_tag_line] server para retornar a lista de valores relacionadas a tag
        #--- esse resposta entra parâmetro na função que "popula" as estruturas [fill]

        self.fill( self.search_tag_line('states', self.dfa_definition)           , self.state_list       )
        self.fill( self.search_tag_line('final_state', self.dfa_definition)      , self.final_state_list )
        self.fill( self.search_tag_line('alphabet', self.dfa_definition)         , self.alphabet_list    )
        self.fill( self.search_tag_line( 'transition_list', self.dfa_definition) , self.production_rules )
 
        #--- because theres only one initial state .-. --- #self.build  ( self.search_tag_line('initial_state', self.dfa_definition)    , self.initial_state    )

        self.initial_state = self.search_tag_line ('initial_state', self.dfa_definition)

        self.root = State(self.initial_state)
        
        #--------------------------------

        #--- rotina simplificada para mostrar o conteudo das estruturas do DFA

        print '+------------------------------------------------+'

        for e in self.__dict__.keys(): #--- retorna todas as estruturas declaradas dentro do objeto
            
            if e in ['dfa_definition' , 'root']: #--- esses dois rotulos não são estruturas lineares

                continue

            print e + ' -> ' , self.__dict__.get(e)[0::1]

        print '+------------------------------------------------+'

        #self.build_dfa(self.root).get_name()
    
    #---------------------------------------------
    #
    #               pre-load builds
    #
    #---------------------------------------------

    def search_tag_line( self , tag , text ):
        
        for l in text.replace('\n','').split(';'):
            
            line_tag = l.split('=')[0].replace(' ','')

            if line_tag == tag:
                
                return l.split('=')[1]
   
    def fill(self, values, struct):

        for v in values.split(','):

            #--- caracteres especiais

            tmp = v.replace(" ","")

            #if tmp == 'SP':

            #   tmp = ' '

            struct.append(tmp)

    #-----------------------------------------------    
    
    def build(self):

        #self.build_dfa(self.root) #--- old call for old build_dfa

        self.root = self.build_dfa()

        return self

    def build_dfa (self):

        print '<building state>'
        
        #--- criando todos os possiveis estados antes nos podemos retirar alguns [if] proxima iteração
        #--- e tamb�mm acaba com o problema se null pointer! uma vez que se deixarmos a criação dos estados
        #--- na iteração normal (1 por 1) quando tiver um estado n referenciando um n+1, aplicariamos a recursão para criarmos ele
        #--- e se o estado n+1 usa-se o estado n entrariamos num loop inifinito
        
        created_states = {}
        
        for state_name in self.state_list :
            
            created_states[state_name] = State(state_name)
            
            if state_name in self.final_state_list :
                
                created_states.get(state_name).set_final(True)
        
        #--- sinalizando o estado inicial corretamente
        
        created_states.get(self.initial_state).set_initial(True)
        
        #--- filling the sttes with their production rules
        
        for state_name in self.state_list :
            
            print '<state><'+state_name+'>',
            
            print '<searching rule>'
            
            for line in self.production_rules :
                
                rule = line.split('->')
                
                #--- rule[0] = state's name in relation with the rule , rule[1] = consume symbol plus produced state
                
                if state_name == rule[0] :                     
                
                    print '<found> '+line
                    
                    rule[1] = rule[1].split(':')
                    
                    consume_symbol = rule[1][0]
                    
                    production_state = created_states.get ( rule[1][1] )
                    
                    if production_state == None :
                        
                        print '<<state doesnt exist>>'
                        
                        exit()
                        
                    created_states.get(state_name).add_production_rule ( consume_symbol , production_state )
                    
        print '<end>'
        
        return created_states.get(self.initial_state)
       

    def get_initial_state(self):

        
        return self.root

#-------------------------------------------------------------------------------
#
#                    Source file to be validate
#
#-------------------------------------------------------------------------------

class Text(object):

    def __init__(self, text):

        self.text = text

        self.index = 0

    def get_next_char(self):

        tmp = self.text[self.index]

        self.index += 1

        return tmp

    def get_index(self):

        return self.index

class Source(object):
    
    def __init__(self, file_path):

        self.original_text = (''.join(open(file_path)))
        
        #--- replacing all the special characters

        self.text = self.original_text.replace(' ','[SPC]').replace('\n','[EOL]').replace(',','[CMA]').replace('(','[OBKT]').replace(')','[CBKT]').replace('.','[DOT')
        
        self.index = 0

    def get_text(self):

        return self.text

    def get_next_char(self):

        #--- fim de fita
        if ( self.index >= len(self.text) ) :  

            return None

        c = self.text[self.index]

        #--- bufferizando caracteres especiais
        if c == '[':

            c = self.special_token_buffer(c)
            
        self.increment_index()

        return c
    
    def special_token_buffer(self, c):

        self.increment_index()

        for nc in range( self.index , len(self.text) ):
            
            c += self.text[nc]

            if self.text[nc] == ']' :

                return c

            self.increment_index()

            

    def increment_index(self):
        
        self.index += 1

    def decrement_index(self):

        self.index -= 1
        
    def get_index(self):
        
        return self.index

class TokenSource(object):

    def __init__(self, file_path):

        self.original_text = ( ''.join( open(file_path) ) ).split('\n')
        
        self.text = []

        self.index = 0

        for elements in self.original_text:
            
            elements = elements.split(':')
            
            if elements[0] == '':

                continue

            self.text.append(elements[0])

    def get_text(self):

        return self.text

    def get_next_char(self):

        if( self.index >= len(self.text)):

            return None

        c = self.text[self.index]

        self.index += 1

        return c


#-------------------------------------------------------------------------------

class Manager(object):

    def __init__(self):

        self.dfa_list = {}

    def add_dfa(self, dfa):

        
        self.dfa_list[dfa.get_name()] = dfa
        

    def get_dfa(self, name):

         
        return self.dfa_list.get(name)
         

    #def validate(self, dfa, source):
    def validate(self, dfa, source):

        return self.vld(dfa.get_initial_state(), source)
        
    def vld(self, state, source):
        
        char = source.get_next_char()
        
        #--- ainda temos caracteres para ler
        
        if( char != None ) :
            print '\n+-------------------------------+'
            print '<reading><'+char+'>\n<index><'+str(source.index)+'> <len><'+str(len(source.text))+'>',
            
            next_state = state.get_next_state( char )
            
            #--- ainda existe estados como respota do consumo?
            
            if ( next_state != None ): #--- sim!
            
                print '\nfrom <'+state.get_name()+'> to <'+next_state.get_name()+'>'
                print '+-------------------------------+\n'
                return self.vld(next_state, source)
            
            else : #--- nao
            
                print '\n<<<no transiction found>>>>\n<<<invalid word>>>>'
                
                return False
            
        #--- nao ha mais caracteres
            
        else :
            
            #--- fim do texto
            
            #--- avaliando o estado no qual o texto terminou
            
            if state.is_final :
            
                print '<valid word>'
                
                return True
            
            else :
            
                print '<invalid word>'
                
                return False
        #TODO verificar validade de  um retorno aqui
        #return True
