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

        for e in self.__dict__.keys(): #--- retorna todas as estruturas declaradas dentro do objeto
            
            if e in ['dfa_definition' , 'root']: #--- esses dois rotulos não são estruturas lineares

                continue

            print e + ' -> ' , self.__dict__.get(e)[0::1]

        #self.build_dfa(self.root).get_name()
    
    #---------------------------------------------
    #
    #               pre-load builds
    #
    #---------------------------------------------

    def search_tag_line( self , tag , text ):
        
        for l in text.replace('\n','').split(';'):
            
            line_tag = l.split('=')[0]
            
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
  
    #--- deprecated algorithm - (no self-consume)
    #def build_dfa (self, state): 
    #    
    #    #--- filling the respective production rules
    #    print 'search production rules for state[' + state.get_name() + ']'
    #    
    #    for line in self.production_rules:
    #        
    #        #print 'rule -> ', line
    #
    #        line = line.split('->')
    #        
    #        if state.get_name() == line[0] :
    #            
    #            print line[1]
    #            
    #            consume_symbol = line[1].split(':')[0]
    #            
    #            production_state = line[1].split(':')[1]
    #            
    #            new_state = State( production_state )
    #
    #            if new_state.get_name() in self.final_state_list:
    #                
    #                new_state.set_final(True)
    #
    #            state.add_production_rule ( consume_symbol , new_state )
    #
    #            print state.get_name() + ' >> ' + new_state.get_name()
    #
    #            print '<< ' + self.build_dfa(new_state).get_name()
    # 
    #    return state

    def build_dfa (self):

        print '<building state>'
        
        #--- criando todos os possiveis estados antes nos podemos retirar alguns [if] proxima iteração
        #--- e também acaba com o problema se null pointer! uma vez que se deixarmos a criação dos estados
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

class Source(object):
    
    def __init__(self, file_path):

        self.original_text = (''.join(open(file_path)))
        
        #--- replacing all the special characters

        self.text = self.original_text.replace(' ','[SPC]').replace('\n','[EOL]').replace(',','[CMA]').replace('(','[OBKT]').replace(')','[CBKT]')
        
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


#-------------------------------------------------------------------------------

class Manager(object):

    def __init__(self):

        self.dfa_list = {}

        self.source = None

    def set_source(self, source):

        self.source = source

    def get_source(self):

        return self.source

    def add_dfa(self, dfa):

        self.dfa_list[dfa.get_name()] = dfa

    def get_dfa(self, name):

        return self.dfa_list.get(name)

    def validate(self, dfa):
        
        print 'run bitch, run!'

        self.vld(dfa.get_initial_state(), self.get_source())

    def vld(self, state, source):

        char = source.get_next_char()
    
        #--- ainda temos caracteres para ler

        if( char != None ) :
            
            print '<reading><'+char+'>\t<index><'+str(source.get_index())+'>\t<len><'+str(len(source.text))+'>',
            
            next_state = state.get_next_state( char )

            #--- ainda existe estados como respota do consumo?

            if ( next_state != None ): #--- sim!

                print 'from <'+state.get_name()+'> to <'+next_state.get_name()+'>'

                self.vld(next_state, source)

            else : #--- nao

                print '\n<no transiction found>\n<invalid word>'

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

#-------------------------------------------------------------------------------
class OldManager(object):

    def __init__(self):

        self.transition_table = [] # the abstraction of production rule table

        self.states           = [] # avaible states on the DFA

        self.final_state      = [] # acceptables states

        self.initial_state    = "" # start point

        self.alphabet         = [] # ...

        self.root_state       = None # root for the automata tree

    def search_transition(self, state_name): # yeah, i'm think why i'm not transporting a Object state .-.

            '''
                Search method on the reachable states on "state_name".
            '''

            print '---------------------------------------\n'\
                  '    BGN  search for a transition       \n'\
                  '---------------------------------------\n'

            print '\n[search transition for] -> '+state_name

            for transitions in self.transition_table:

                print '\n\t[reading] -> '+transitions

                splited_transition = transitions.split("->")

                # here we read every element on the transition_table
                # the format of this elements are: [label_actual_state] -> [label_symbol] : [label_next_state]
                #
                # like a : Foo -> lu : Boo
                #
                # so we need to know with the [label_actul_state] is the same for the name passed on args
                # if it is we got the correct ruler of production for this state!
                #

                if splited_transition[0] == state_name:

                    print '\n\t\t[found a rule]'

                    consume_symbol = splited_transition[1].split(":")[0]

                    production_state_name = splited_transition[1].split(":")[1]

                    print '\n\t\t\tif i\'m on ['+state_name+'] and read ['+consume_symbol+'] i\'m going to ['+production_state_name+']'

                    print '\n---------------------------------------\n'\
                          '    END  search for a transition       \n'\
                          '---------------------------------------\n'

                    return [consume_symbol,production_state_name]

                else : # its a linear search dude! we need to test ALL the thing

                    continue

                return None

    #def build_dfa(self,state): # here is a try to build the virtual DFA on a "elegant" recursively method

            if state == None:

                # so we think... there are a self.root on attribute yeah?
                #
                # yeah.
                #
                # that self.root needs to be the "head" that points for the real "first state" on DFA
                # and this is why we use ini_state buff?
                # i am affraid not.i
                #
                # see the load_af_file method
                # he calls this and keep the returnin on the root node! so the mothafocka self.root is the zero state

                print '\n----------------------------\n'\
                      '      [build AF first run]'\
                      '\n----------------------------\n\n'\
                      '\tCreating Initial state with name ['+self.initial_state+']'

                ini_state = State(self.initial_state)

                print '\n[calling recursion]'

                self.build_dfa(ini_state)

                return ini_state

            else:

                # here is the recursive part actived by the direct calling on first run

                actual_state = state.get_state_name()

                print '\n[state] -> ['+actual_state+']'

                print '\n\t[load transition_table and  search for a production rule]'

                tmp = self.search_transition(actual_state)

                # before 05/03/2012 we returning void from the method search_transition when he not found production
                # now the dude return None object .-.
                # so we need a treatment for this null point (java fellings >.<)

                if tmp == None:

                    exit()

                print '\n[creating transition] -> ['+actual_state+'] -> ['+tmp[0]+'] : ['+tmp[1]+']'

                print '\n\t[adding rule] '+'\"['+actual_state+'] -> ['+tmp[0]+'] = ['+tmp[1]+']\"'+'to state ['+actual_state+']'

                n_state = State(tmp[1])

                #print n_state.get_state_name()

                state.add_transition(tmp[0], n_state)

                if tmp[1] in self.final_state:

                    print '\n\t\t\t[final state ['+n_state.get_state_name()+']] AF needs to die here .-.\n'

                    return None

                else:

                    self.build_dfa(n_state)

    def formatting_file(self, filepath):

        t = ''

        for lines in filepath:

            t += lines

        t = t.replace(" ", "").replace("\n", "")

        return t

    def formatted_test(self, filepath):

        result_set = {}

        result_string_list = []

        final_result = []

        t = self.formatting_file(filepath)

        print '[searching for test tag]'

        for sentence in t.split(";"):

            tag = sentence.split("=")[0]

            if tag != '':

                value = sentence.split("=")[1]

            else :

                continue

            print '[tag] -> '+tag

            print '[value] -> '+value

            if tag == 'test':

                for v in value.split(','):

                    string = v.split(':')[0]

                    val = v.split(':')[1]

                    if val == 't':

                        val = True

                    else:

                        val = False

                    result_set[string] = val

                    result_string_list.append(string)

                #FOR

            #END

        #FOR

        print '\n\n[Begging Tes]\n\n'

        for word in result_string_list:

            x = self.validate(0, word, None)

            print '~>'+str(x)

            if x == True:


                if result_set.get(word) == True:

                    final_result.append((word, str(result_set.get(word)), str(x)))

                else:

                    final_result.append((word, str(result_set.get(word)), str(x)))

            else:

                if result_set.get(word) == True:

                    final_result.append((word, str(result_set.get(word)), str(x)))

                else:

                    final_result.append((word, str(result_set.get(word)), str(x)))

        #FOR

        print Ascii.print_table(['string','to be', 'got'], final_result)


    def load_dfa_definition_file(self, filepath):

        print '\n\n\nBGN [loading table]\n\n\n'

#        t = ''
#
#        for lines in filepath:
#
#            t += lines
#
#        t = t.replace(" ", "").replace("\n", "")

        t = self.formatting_file(filepath)

        print '[formatted text without spaces]\n'

        for sentence in t.split(";"):

            print '\n----[sentence analisis]'

            print '\n\t[reading sentence] -> '+sentence

            tmp = sentence.split("=")

            print '\n\t[splitting sentence] -> ' + str(tmp)

            if len(tmp) == 1:

                print '[non valid sentence] break process'

                break

            else:

                print '\n----[tag analisis]'
                print '\n\t[reading]'
                print '\n\t\t[tag] -> '+tmp[0]
                print '\n\t\t[values] -> '+tmp[1]

                for value in tmp[1].split(','):

                    #swicth = {'states':self.states.append(value),'final_state':self.final_state.append(value),'alphabet': self.alphabet.append(value), 'transition_list' : self.transition_table.append(value)}

                    #swicth.get(tmp[0])

                    print '\n----[storing]'

                    print '\n\t[value] -> '+value+' [on] '+tmp[0]

                    if tmp[0] == 'states':

                        self.states.append(value)

                    elif tmp[0] == 'final_state':

                        self.final_state.append(value)

                    elif tmp[0] == 'initial_state':

                        self.initial_state = value

                    elif tmp[0] == 'alphabet':

                        self.alphabet.append(value)

                    elif tmp[0] == 'transition_list':

                        self.transition_table.append(value)

                    else:

                        continue

                print '\n\n--------[New Loop]\n\n'
        #END FOR

        print '\n----[structs]'

        print '[alphabet]\t\t'+str(self.alphabet)+'\n'\
              '[states]\t\t'+str(self.states)+'\n'\
              '[final_state]\t\t'+str(self.final_state)+'\n'\
              '[transitiontable]\t'+str(self.transition_table)+'\n'

        print '\n\n\nEND [loading table]\n\n\n'

        self.root_state = self.build_dfa(None)

    #--- END load_file DEF -------------------------------------------------

    def validate(self,read_index,word,state):

        print '\n[index] '+str(read_index+1)+'/'+str(len(word))+' [word size]'

        if state == None and read_index == 0:

            print '\n---------------------------------------'\
                  '\n             BGN  Validating           '\
                  '\n---------------------------------------\n'

            next_state = self.root_state.get_next_state(word[read_index])

            print '\n\t['+self.root_state.get_state_name()+'] -> ['+word[read_index]+'] : ['+next_state.get_state_name()+']'

            print  '\n\n\t\t[looking for next state]'

        else:

            if read_index == len(word):

                return

            print '--------------------------------------'
            print '\nstate ['+state.get_state_name()+']'\
                  '\n\t['+state.get_state_name()+'] -> ['+word[read_index]+'] : [?]'\
                  '\n\n\t\t[looking for next state]'

            next_state = state.get_next_state( word[read_index] )

            print '\n\t\t\t['+next_state.get_state_name()+']'

        if next_state == None :#or ( next_state != None and (read_index + 1) == len(self.transition_table) ):

            print '\n\t\t\t[404][transition not found] word cannot be validated on AF'

            return False

        elif next_state.get_state_name() in self.final_state:

                print '\n\t\t\t\t[valid word!] next state is a final state'

                return True

# - Deprecated - first model for valid finalstate!
#        if read_index == len(word) - 1:
#
#            if next_state.get_state_name() in self.final_state:
#
#                print 'Next state is ['+next_state.get_state_name()+'] and is satisfatory state ;D'
#
#                return True
#
#            else:
#
#                print 'Invalid Word!\nNo transition was found for consume ['+word[read_index]+']'
#
#                return False

        read_index+=1

        print '\n\t\t\t\t Found!'

        print '--------------------------------------'

        return self.validate(read_index,word,next_state)

