# --- Misc functions ---------------------------------------------------

def file_to_string( file_path ):
    
    if file_path == '':
        
        print 'fuck! this is a empity address .-.'
        exit( 0 )
    
    else :
        
        return ''.join( open( file_path ) )

# ----------------------------------------------------------------------

class RegularGrammar():
    
    def __init__( self ):
        
        # The original text from .gr files

        self.general_definition = ""

        # The "macro/label/variables" table :D

        self.nonterminal_table = {}  

        self.alphabet = []

        self.state_qtt = 0 #rename it

        print 'stuff'

# --------------------------------------------------------------------- 
# --------------------------------------------------------------------- 

    def build_nonterminal_table( self ):
                
        # we dont need to worry about the white space ! :D
        # we can clean the whitespace and then split on the ";" (semicolon)
        
        general_definition_byline = self.general_definition.replace( ' ' , '' ).replace( '\n' , '').split( ';' )
        
        general_definition_byline = general_definition_byline[ 0 : ( len(general_definition_byline) - 1  )  ]

        for line in general_definition_byline :
            
            print '\n' , 'processing line [' , line , ']'

            variable_name , value = line.split( ':' )

            print '\n' , 'variable_name -> ' , variable_name , '\n' , \
                  'value         -> ' , value

            # --- saving :D

            self.nonterminal_table[ variable_name ] = value

        # --- generating alphabet

        for variable_name in self.nonterminal_table.keys():

            value = self.nonterminal_table.get( variable_name )

            value = value.replace( ',' , ' ' ).replace( '|' , ' ' )

            value = value.split(' ')

            for token in value :

                print '[' , token  , ']' , 'terminal?',

                if token in self.nonterminal_table.keys():

                    print 'yes @_@' 

                else :

                    print 'no ^_^'

                    self.alphabet.append( token )

        print '\n+------------------------+\n' , \
              '|      The alphabet      |\n' , \
              '+------------------------+'

        print self.alphabet

# --------------------------------------------------------------------- 
# --------------------------------------------------------------------- 
    def build_afd( self ):
        
        alphabet_section = self.formmating_alphabet()
        
        transition_list  = self.formmating_transition_list()

        state_list       = self.formmating_state_list()

                

        print '-------------'  , '\n' ,\
              alphabet_section , '\n' ,\
              state_list       , '\n' ,\
              transition_list  , '\n' ,\
              '------------'

        initial_state = 'initial_state = TODO ;'
        final_state   = 'final_state = TODO ;'


        return state_list +'\n'+ alphabet_section +'\n'+ initial_state +'\n'+ final_state +'\n'+ transition_list + '\n'

    def formmating_alphabet( self ):

        text_tmp = ''

        for token in self.alphabet : 

            if self.alphabet.index( token ) == ( len( self.alphabet ) - 1 ):
    
                text_tmp += token + ';'

            else :

                text_tmp += token + ','

        text_tmp = 'alphabet = ' + text_tmp
         
        return text_tmp

    def formmating_transition_list( self ):
        
        tmp = self.fuckoff2( 0 ,'afd')
        
        tmp = self.ambiguous_remover( tmp )
        
        tmp22 = ''
        
        for shit in tmp :
            
            tmp22 += shit + '\n' 
        
        return 'transition_list = \n'+tmp22+'\n;'
    
    def formmating_state_list( self ):

        state_list  = str (range( 0 , self.state_qtt+1 ))
    
        state_list = state_list.replace( '[' , '' ).replace( ']' , '')

        return 'states = ' + state_list + ';'

    def ambiguous_remover( self , text ):
        
        linebuffer = []
        
        for line in text.split( '\n' ):
            
            if not line in linebuffer and line != '':
                
                linebuffer.append( line )
        
        return linebuffer
        
    
    def fuckoff2 ( self , state , nonterminal_label ):
        
        refrmt = lambda x : x.replace(',',' , ').replace('|',' | ')
        
        production_string = self.nonterminal_table.get(nonterminal_label)
        
        production_list = refrmt(production_string).split(' ')
        
        reformated_production_string = ''
        
        state_counter = state
        
        count = 0
        
        end = ( len( production_list ) - 1 )
        
        operator_ahead = ''
        
        for token in production_list:
            
            # --- verifying for non-terminal
            
            if token in self.nonterminal_table.keys() :
                
                reformated_production_string += self.fuckoff2( state_counter , token )
                    
            else :
                
                if not token in [',','|']:
                
                    if not count == end :
                        
                        reformated_production_string += str( state_counter ) + '->' + token + ':' + str ( (state_counter + 1) ) + '\n'
                        
                    else :
                        
                        reformated_production_string += str( state_counter ) + '->' + token + ':' + str ( state ) + '\n'
                
                    try :
                    
                        if production_list[ count + 1 ] == ',' : # --- verificando o operator
                    
                            state_counter += 1
                            
                    except :
                    
                        pass
                    
            print state_counter
            
            self.biggest_state_created( state_counter )

            count += 1
            

        
        return reformated_production_string


    def biggest_state_created( self , state ):

        if int( state ) > self.state_qtt :

            self.state_qtt = state

if __name__ == '__main__' :
    
    
    # rodar verficacao de ambiguidade antes do precesso de persistencia do arquivo!!!!!!!!
    #
    
    gr = RegularGrammar()
    
    tmp = file_to_string( 'lua.cfg' )
    
    gr.general_definition = tmp 
    
    gr.build_nonterminal_table()
    
    #print '+---------------------------+'
    
    text = gr.build_afd()
    
    print '========================='
    
    print text

    #print '========================='
