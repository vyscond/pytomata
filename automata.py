# -*- coding: iso-8859-1 -*


# O legal foi que conseguistes criar um estrtura bem generica na aplicacao
# dos testes.
# 
# Criastes um padrao simples, estupido e besta para abstrair cada tipo de
# texto que pode ser validado com o AFD!
# 
# Bom, qualquer usuario pode criar um objeto independente deste pacote e usa-lo
# como teste :D basta escrever as interfaces :D


'''
Created on Feb 20, 2012

@author: abara
'''

#-------------------------------------------------------------------------------
#--- Misc Config ---------------------------------------------------------------
#-------------------------------------------------------------------------------
def search_tag_line(tag , text ):

        for line in text.replace('\n','').split(';'):
            
            line_tag = line.split('=')[0].replace(' ','')
        
            if line_tag == tag:
        
                return line.split('=')[1]
   
def fill(values, struct) :
    
    for element in values.split(','):
   
        #--- caracteres especiais
        
        tmp = element.replace(" ","")
        
        #if tmp == 'SP':
        
        #   tmp = ' '
        
        struct.append(tmp)

#-------------------------------------------------------------------------------

class State(object):

    def set_initial(self, initial):
        
        '''
            Set this state as initial {yes : True, no : False}
        '''
        
        self.initial = initial
    
    def is_initial(self):
        
        '''
            check if the state is initial
        '''
        
        return self.initial
    
    def set_final(self, final):
        
        '''
            Set this state as final {yes : True, no : False}
        '''
        
        self.final = final
        
    def is_final(self):
        
        '''
            check if the state is final
        '''
        
        return self.final

    def __init__(self, state_name):
        
        self.final = False
        
        self.initial = False
        
        self.state_name = state_name
        
        self.transition_states = {}
        
    def get_name(self):
        
        '''
            get the State's name
        '''
        
        return self.state_name
        
    def add_production_rule(self, consume_symbol, state):
        
        '''
            Add a new production
        '''
        
        self.transition_states[consume_symbol] = state
        
    def get_next_state(self, consume_symbol):
        
        '''
            Get the next state based on symbol that was readed
        '''
        
        return self.transition_states.get(consume_symbol)

class DeterministicFiniteAutomata(object):
    
    def get_name(self):
  
        '''
            get the name of this DFA
        '''
        
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
        
        self.dfa_definition = ''.join(open(dfa_file_path)).replace(' ','')
        
        #----------------------------------------------------------
        #
        #                     filling structs
        #
        #----------------------------------------------------------
        
        #--- a funcao [search_tag_line] server para retornar a lista de valores relacionadas a tag
        #--- esse resposta entra como par�metro na funcao [fill] que preenche as estruturas 
        
        
        
        fill( search_tag_line( 'states'          , self.dfa_definition) , self.state_list       )
        fill( search_tag_line( 'final_state'     , self.dfa_definition) , self.final_state_list )
        fill( search_tag_line( 'alphabet'        , self.dfa_definition) , self.alphabet_list    )
        fill( search_tag_line( 'transition_list' , self.dfa_definition) , self.production_rules )
        
        #--- because theres only one initial state .-. ---
        #self.build  ( self.search_tag_line('initial_state', self.dfa_definition)    , self.initial_state    )
        
        self.initial_state = search_tag_line ('initial_state', self.dfa_definition)
        
        self.root = State(self.initial_state)
        
        #---------------------------------------------------------------------
        #---------------------------------------------------------------------
        #
        #  rotina simplificada para mostrar o conteudo das estruturas do DFA
        #
        #---------------------------------------------------------------------
        #---------------------------------------------------------------------
        
        print '+------------------------------------------------+'
        
        #--- retorna todas as estruturas declaradas dentro do objeto
        for attribute_name in self.__dict__.keys(): 
            
            #--- esses dois rotulos nao sao estruturas lineares
            if attribute_name in ['dfa_definition' , 'root']: 
        
                continue
        
            print attribute_name + ' -> ' , self.__dict__.get(attribute_name)[0::1]
        
        print '+------------------------------------------------+'
        
        #self.build_dfa(self.root).get_name()

#-----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------

    #---------------------------------------------
    #
    #               pre-load builds
    #
    #---------------------------------------------
    
    def build(self):

        #self.build_dfa(self.root) #--- old call for old build_dfa
        
        self.root = self.build_dfa()
        
        return self

    def build_dfa (self):

        print '--- building state ---'
        
        # Ao criarmos todos os possiveis estados antes, nos possibilitamos a retirada de alguns [if] no proximo processo de iteracao
        # e tamb�m acaba com o problema de null pointer! uma vez que se deixarmos a cria��o dos estados
        # na itera��o normal (1 por 1) quando tiver um estado n referenciando um n+1, aplicariamos a recurs��o para criarmos ele
        # e se o estado N+1 usasse o estado N entrariamos num loop inifinito
        # --- e assim ele falou :D --- and its true !!!
        
        created_states = {}
        
        for state_name in self.state_list :
            
            created_states[state_name] = State(state_name)
            
            if state_name in self.final_state_list :
                
                created_states.get(state_name).set_final(True)
        
        #--- sinalizando o estado inicial corretamente
        # man, why the fuck this is out from the upper IF? uu'
        
        created_states.get(self.initial_state).set_initial(True)
        
        #--- filling the sttes with their production rules
        
        for state_name in self.state_list :
            
            print '[state] -> <'+state_name+'>',
            
            print '>>> searching rule'
            
            for line in self.production_rules :
                
                rule = line.split('->')
                
                #--- rule[0] = state's name in relation with the rule , rule[1] = consume symbol plus produced state
                
                if state_name == rule[0] :                     
                
                    print '[found] -> <'+line+'>'
                    
                    rule[1] = rule[1].split(':')
                    
                    consume_symbol = rule[1][0]
                    
                    production_state = created_states.get ( rule[1][1] )
                    
                    if production_state == None :
                        
                        print '<<< state doesnt exist!'
                        
                        exit()
                        
                    created_states.get(state_name).add_production_rule ( consume_symbol , production_state )
                    
        print '<<< end'
        
        return created_states.get(self.initial_state)
       

    def get_initial_state(self):

        
        return self.root

#-------------------------------------------------------------------------------
#
#                    Source file to be validate
#
#-------------------------------------------------------------------------------

class Text(object):
    
    '''
        Abstracting a simple text for the automata motor
    '''
    
    def __init__(self, text):

        self.text = text

        self.index = 0

    def get_next_char(self):

        tmp = self.text[self.index]

        self.index += 1

        return tmp

    def get_index(self):

        return self.index


class TokenSource(object):
    
    '''
        Formmating .lex file to being parser text
    '''
    
    def __init__(self, tokenlist ):
        
        self.original_text = ''
        
        # --- isso aqui da mais liberdade no formato de entrada ;D
        # --- if/else mais simple de entender do que um try/catch so... gfys
        
        if type( tokenlist ) == type( '' ) :
            
            self.original_text = tokenlist.split('\n')
        
        else:
            
            self.original_text = ''.join( tokenlist ).split('\n')
            
        
        self.text = []
        
        self.index = 0
        
        for elements in self.original_text:
            
            elements = elements.split(':')
            
            if elements[0] == '':

                continue
            
            elif elements[0] == 'reserved_word':
                
                self.text.append(elements[1])
                
            else :
                
                self.text.append(elements[0])

    def get_text(self):

        return self.text

    def get_next_char(self):

        if( self.index >= len(self.text)):

            return None

        char = self.text[self.index]

        self.index += 1

        return char

#-----------------------------------------------------------------------------------------------
#===============================================================================================
#-----------------------------------------------------------------------------------------------

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
            
            print '[READING] -> <'+char+'>  [LENGTH] -> ' , len(source.text) , '/' , source.index , '\n'
            
            next_state = state.get_next_state( char )
            
            #--- ainda existe estados como respota do consumo?
            
            if ( next_state != None ): #--- sim!
            
                print '[ACTUAL STATE] -> ['+state.get_name()+'] [GOING TO] -> ['+next_state.get_name()+']'
                print '\n>>> recursion\n'
                return self.vld(next_state, source)
            
            else : #--- nao
            
                print '\n<<<no transiction found\n[INVALID WORD]'
                
                return False
            
        #--- nao ha mais caracteres
            
        else :
            
            #--- fim do texto
            
            #--- avaliando o estado no qual o texto terminou
            
            if state.is_final :
            
                print '[VALID WORD]'
                
                return True
            
            else :
            
                print '[INVALID WORD]'
                
                return False
        #TODO verificar validade de  um retorno aqui
        #return True
        
        
#-----------------------------------------------------------------------------------------------
#===============================================================================================
#-----------------------------------------------------------------------------------------------

# --- this shit is deprecated ;D

#-----------------------------------------------------------------------------------------------
#===============================================================================================
#-----------------------------------------------------------------------------------------------

#class Source(object):
    
    #def __init__(self, file_path):

        #self.original_text = (''.join(open(file_path)))
        
        ##--- replacing all the special characters

        #self.text = self.original_text.replace(' ','[SPC]').replace('\n','[EOL]').replace(',','[CMA]').replace('(','[OBKT]').replace(')','[CBKT]').replace('.','[DOT')
        
        #self.index = 0

    #def get_text(self):

        #return self.text

    #def get_next_char(self):
        
        #'''
            #Will mask the entire text, including the special tokens, as a literal char sequence text
        #'''
        
        ##--- fim de fita
        #if ( self.index >= len(self.text) ) :  

            #return None

        #char = self.text[self.index]

        ##--- bufferizando caracteres especiais
        #if char == '[':

            #char = self.special_token_buffer(char)
            
        #self.increment_index()

        #return char
    
    #def special_token_buffer(self, special_token):
        
        #'''
            #Buffering the string that begins with '[' delimiter
        #'''
        
        #self.increment_index()

        #for char in range( self.index , len(self.text) ):
            
            #special_token += self.text[char]
            
            #if self.text[char] == ']' :
            
                #return special_token
            
            #self.increment_index()
            
    #def increment_index(self):
        
        #self.index += 1
    
    #def decrement_index(self):
        
        #self.index -= 1
        
    #def get_index(self):
        
        #return self.index
