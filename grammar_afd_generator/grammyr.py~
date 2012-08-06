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

        self.variable_table = {}

        self.alphabet = []

        self.last_biggest_state = 0

        print 'stuff'

    #------------
    # Running ok
    #------------
    def build_variable_table( self ):
                
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

            self.variable_table[ variable_name ] = value

        # --- generating alphabet

        for variable_name in self.variable_table.keys():

            value = self.variable_table.get( variable_name )

            value = value.replace( ',' , ' ' ).replace( '|' , ' ' )

            value = value.split(' ')

            for token in value :

                print '[' , token  , ']' , 'terminal or non-terminal?',

                if token in self.variable_table.keys():

                    print 'yes @_@' 

                else :

                    print 'no ^_^'

                    self.alphabet.append( token )

        print '\n+------------------------+\n' , \
              '|      The alphabet      |\n' , \
              '+------------------------+'

        print self.alphabet



    def build_afd( self ):
        
        # --------------------------------------------------------------------------
        # 08/01/2012 - 15:10
        # we need to setup a "begin" flag on the many token we can have on the file
        # this flags is AFD ;D
        # -------------------------------------------------------------------------

        # FINDING THE AFD FLAG ;D
        
        afd_text = ''

        # --- writing alphabet

        afd_text += self.formmating_alphabet() + '\n\n'

        afd_text += 'transition_list = \n' + self.build_path( 0 , 'afd' ) + '\n;'

        return afd_text

    #------------
    # Running ok
    #------------

    def formmating_alphabet( self ):

        text_tmp = ''

        for token in self.alphabet : 

            if self.alphabet.index( token ) == ( len( self.alphabet ) - 1 ):
    
                text_tmp += token + ';'

            else :

                text_tmp += token + ','



        text_tmp = 'alphabet = ' + text_tmp
        
        print 'last state ', self.last_biggest_state

        return text_tmp


    # -------------------------------------------------------------------
    # 08/01/2012 - 14:30
    # nigga! we need to think about the ideia to using the lexy2 to build
    # a valid and formated output to this process.
    # But we will not need stuff like "a:identifier" , got it?
    # think about.
    # -------------------------------------------------------------------
    # 08/01/2012 - 15:00
    # Lol no! I got it now ;D

    # fix the correct number state for the last element from a recusion

    def build_path( self , last_state , variable_name  ):

        state_base_number = last_state + 1
        
        value = self.variable_table.get( variable_name )
        
        value = value.split( ',' )

        afd_text = ''

        # now we know the sequence to "concat" the things .-.
        # with this we will worry about the "|" (or) sentences ;D
        
        for line in value :

            print 'processing -> [' , line , ']'
            
            if '|' in line : 

                # 08/01/2012 - 16:32
                # Descobre o ponto de corte ;D Ha! I double dare you ;3

                for token in line.split( '|' ):
                    
                    if value.index( line ) == ( len( value ) - 1 ):
                        
                        afd_text += str( state_base_number ) + '->'  +  token + ':' + str( last_state + 1 ) + '\n'

                    else :

                        afd_text += str( state_base_number ) + '->'  +  token + ':' + str( state_base_number + 1 ) + '\n'
                
                state_base_number += 1

            elif line in self.variable_table.keys() :

                #afd_text += '\n' + self.build_path( state_base_number - 1 , line)
                self.last_biggest_state = state_base_number
                afd_text += '\n' + self.build_path( self.last_biggest_state - 1 , line) # --- bleeding edge line

            else :
                
                #if value.index( line ) == ( len( value ) - 1 ):
                #        
                #    afd_text += str( state_base_number ) + '->'  +  line + ':' + str( last_state + 1 ) + '\n'
                #
                #else :

                afd_text += str( state_base_number ) + '->'  +  line + ':' + str( state_base_number + 1 ) + '\n'

               
                state_base_number += 1
        print 'base number --->>> ' , state_base_number , self.last_biggest_state
        if self.last_biggest_state < state_base_number: # --- bleeding edge line

            self.last_biggest_state = state_base_number
             
        return afd_text

