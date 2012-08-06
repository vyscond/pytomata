# -*- coding: iso-8859-1 -*

def file_to_string( file_path ):
    
    return ( ''.join( open(file_path) ) )
    
#-------------------------
#
# --- core file filler ---
#
#-------------------------

def fill(tag , text ):
    
    for line in text.replace('\n','').split(';'):
        
        # --- line -> " tag_line = something1 , something2 "
        
        line_tag = line.split('=')[0].replace(' ','')
        
        if line_tag == tag:
            
            # --- [ something1 , something2 , ... ]
            
            line_tag_content = line.split('=')[1].split(',') 
            
            content_list = []
            
            for content in line_tag_content :
                
                content_list.append( strip( content ) )
    
    return content_list
    

def default_identifier_format_checker( text ):
    
    if text[0].isalpha() and len( text ) == 1 :
        
        return True
        
    return True if ( text[0].isalpha() and text[1: (len( text ) - 1) ].isalnum() ) else False
    

def default_floating_format_checker( text ) :
    
    DOT = False
    
    for char in text :
        
        if char == '.' :
            
            if not DOT :
                
                DOT == True
                
            else :
                
                return False
        
        elif not char in ['1','2','3','4','5','6','7','8','9','0'] :
            
            return False
            
        
    
    return True

def default_integer_format_checker( text ) :

    return True if ( unicode(text) ).isnumeric() else False

class Token():
    
    def __init__(   self , name , lexeme ):
        
        self.name   = name
        
        self.lexeme = lexeme
        

class Scanner():
    
    def __init__( self , lex_definition ):
        
        self.line_counter = 0
        
        self.symbol_table = {}
        
        self.TOKENLIST_TEXT = ''
        
        self.SYMBOL_TABLE = {}
        
        # --- dinamic definitions ---
        
        self.symbols_dictionary = {}
        
        if type( lex_definition ) == type( '' ) :
            
            self.build_symbol_dictionary ( lex_definition )
            
        else :
            
            self.build_symbol_dictionary ( ( ''.join( open ( lex_definition ) ) ) )
            
        #print self.symbol_table
        
    #-------------------------------------------------------------------------------------------
    #                                                                                           
    #           --- Gerando dicionario de pesquisa para a geração da tabela de simbolos ---     
    #                                                                                           
    #-------------------------------------------------------------------------------------------
        
    def build_symbol_dictionary ( self  , text ):
        
        print '[STARTING] [function] \'build_symbol_dictionary\''
        
        text = text.replace('\n','').replace(' ','')
        
        # --- collecting tags
        
        for line in text.split(';'):
            
            if line == '' :
                
                continue
                
            # line template in process -->> " tag_line = something1 , something2 "
            
            line_tag = line.split('<-')[0]# .replace(' ','') --- no more necessary. the whitespaces gone at the firs line!!!
            
            # ----------------------------------------------------------------------------------
            # criando a referencia real dos delimitadores
            # ----------------------------------------------------------------------------------
            
            if line_tag == 'delimiter' :
                
                delimiters_tags = { 'comma' : ',' , 'open_bracket' : '[' , 'close_bracket' : ']' , 'open_key' : '{' , 'close_key' : '}' , 'open_parenthesis' : '(', 'close_parenthesis' : ')', 'dot_comma' : ';' , 'dot' : '.' }
            
            print '\n[SCANNING CONTENT FOR] -> ' , line_tag , '\n'
            
        # --- [ something1 , something2 , ... ]
            
            line_tag_content = line.split('<-')[1].split(',') 
                
            for content in line_tag_content :
                
                content = content#.strip() --- no more necessary. the whitespaces gone at the firs line!!!
                
                # ------------------------------------------------------------------------------
                # Deve haver um processo separado para as marcações de delimitarores
                # umas vez que eles não são definidos na folha de configuração de forma direta
                # ------------------------------------------------------------------------------
                
                if line_tag == 'delimiter' :
                    
                    content = delimiters_tags.get( content )
                
                print '[WRITING] <content><'+content+'> <tag><'+line_tag+'>'
            
                self.symbol_table[ ( content ) ] = line_tag
                
        print '[END] function \'build_symbol_dictionary\'\n'
        
    #-------------------------------------------------------------------------------------------
    #                                                                                           
    #                           --- Gerador de Lista de Tokens ---                              
    #                                                                                           
    #-------------------------------------------------------------------------------------------
    def generate_token_list( self , source_code ):
        
        print '[START] function \'generate_token_list\'\n'
        source_code += '\n'
        source_code = source_code.split('\n')
        
        # --  now we can control the line number for the error output messages
        
        TOKENLIST_TEXT = ''
        
        SYMBOL_TABLE = {}
                
        READING_HEAD_BUFFER = ''
        
        SINGLE_QUOTATION_MARK = False
        
        DOUBLE_QUOTATION_MARK = False
        
        SCAPE_SEQUENCE = False
        
        LAST_TOKEN_TYPE_READED = ''
        
        for source_line in source_code :
            
            self.line_counter += 1
            
            print '[READING LINE] -> ' + source_line
            
            source_line += ' '
            
            for character in source_line:
                
                
                print '+-----------------------------------------------------------------------+\n'\
                      '| [READ]   [' + character + ']\n'\
                      '|                                                                        \n'\
                      '| [BUFFER] [' + READING_HEAD_BUFFER + ']\n'\
                      '+-----------------------------------------------------------------------+\n'
                
                
                # --- we need to check if we found a delimiter or what it is!!!? yeah, this is what i think
                
                if character == ' ' :
                    
                    if SINGLE_QUOTATION_MARK == True :
                        
                        # --- string buffering! keep reading!!!
                        
                        READING_HEAD_BUFFER += character
                        
                        continue
                        
                    elif DOUBLE_QUOTATION_MARK == True :
                        
                        # --- string buffering! keep reading!!!
                        
                        READING_HEAD_BUFFER += character
                        
                    elif READING_HEAD_BUFFER != '' :
                        
                        print '[SAVING BUFFER]'
                        
                        LAST_TOKEN_TYPE_READED = token_type = self.symbol_table.get( READING_HEAD_BUFFER )
                        
                        if token_type == None : # --- this buffer is a numeric constant or an ID
                        
                            # --- verifying as an ID, integer or floating
                            
                            print '[verifying for ID]'
                            
                            if default_identifier_format_checker ( READING_HEAD_BUFFER ) :
                                
                                LAST_TOKEN_TYPE_READED = token_type = 'identifier'
                                
                            print '[verifying for floating constant]'
                            
                            if default_floating_format_checker ( READING_HEAD_BUFFER ) :
                                
                                LAST_TOKEN_TYPE_READED = token_type = 'float'
                                
                            print '[verifying for integer constant]'    
                            
                            if default_integer_format_checker ( READING_HEAD_BUFFER ) :
                                
                                LAST_TOKEN_TYPE_READED = token_type = 'integer'
                                
                            if token_type == None :
                            
                                print 'dont know what is that .-.'
                            
                                exit(0)
                            
                            SYMBOL_TABLE [ READING_HEAD_BUFFER ] = token_type
                                
                            TOKENLIST_TEXT += READING_HEAD_BUFFER + ':' + token_type + '\n'
                                
                            READING_HEAD_BUFFER = ''
                            
                        else :
                            
                            SYMBOL_TABLE[ READING_HEAD_BUFFER ] = token_type
                            
                            TOKENLIST_TEXT += READING_HEAD_BUFFER + ':' + token_type + '\n'
                            
                            READING_HEAD_BUFFER = ''
                
                # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                
                elif character == '\'' :
                    
                    # --- buffering string
                    
                    if SCAPE_SEQUENCE :
                        
                        READING_HEAD_BUFFER += character
                        
                        SCAPE_SEQUENCE = False
                        
                    elif SINGLE_QUOTATION_MARK :
                        
                        if DOUBLE_QUOTATION_MARK :
                            
                            print '[ERROR] [LINE ' , self.line_counter ,'] a double_quote mark is still opened! '
                            
                            exit(0)                        
                        
                        SYMBOL_TABLE[ READING_HEAD_BUFFER ] = 'string'
                        
                        TOKENLIST_TEXT += READING_HEAD_BUFFER + ':' + 'string' + '\n'
                        
                        READING_HEAD_BUFFER = ''
                        
                    SINGLE_QUOTATION_MARK = not SINGLE_QUOTATION_MARK
                
                # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                
                elif character == '\"' :
                    
                    if SCAPE_SEQUENCE :
                        
                        READING_HEAD_BUFFER += character
                        
                        SCAPE_SEQUENCE = False
                        
                    elif DOUBLE_QUOTATION_MARK :
                        
                        if SINGLE_QUOTATION_MARK :
                            
                            print '[ERROR] [LINE '+ self.line_counter +'] a single_quote mark is still opened! '
                            
                            exit(0)
                    
                        SYMBOL_TABLE[ READING_HEAD_BUFFER ] = 'string'
                        
                        TOKENLIST_TEXT += READING_HEAD_BUFFER + ':' + 'string' + '\n'
                        
                        READING_HEAD_BUFFER = ''
                    
                    print DOUBLE_QUOTATION_MARK
                    
                    DOUBLE_QUOTATION_MARK = not DOUBLE_QUOTATION_MARK
                    
                    print DOUBLE_QUOTATION_MARK
                    
                # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                
                elif character == '\\':
                    
                    if SINGLE_QUOTATION_MARK or DOUBLE_QUOTATION_MARK :
                        
                        SCAPE_SEQUENCE = True
                        
                    else :
                        
                        print '[ERROR] [LINE ' , self.line_counter , '] scape_sequence mark out of a string'
                        
                        exit(0)
                
                # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                
                # ------------------------------------------------------------------------------
                # Por alguns erros de lógica vamos ter que criar uma verificação , ate este ponto,
                # redundante para acharmos os outros tipo de delimitadores!
                #
                # Perceba que não estamos nem bufferizando esse caractere especial!
                # ------------------------------------------------------------------------------
                
                # TODO - dude! temos um problema com o reconhecimento de pontos flutuantes!
                
                elif self.symbol_table.get( character ) == 'delimiter' :
                    
                    print '[FOUND] Terminal Delimiter'
                    
                    SYMBOL_TABLE[ character ] = 'delimiter'
                    
                    TOKENLIST_TEXT += character + ':' + 'delimiter' + '\n'
                    
                
                # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                
                else :
                    
                    READING_HEAD_BUFFER += character
                    
                    print source_line.index(character) , len( source_line )
                    
                # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                
        #print TOKENLIST_TEXT
        
        TOKENLIST_TEXT += 'EOF'
        
        print TOKENLIST_TEXT
        
        print SYMBOL_TABLE
        
        self.TOKENLIST_TEXT = TOKENLIST_TEXT
        
        self.SYMBOL_TABLE = SYMBOL_TABLE
        
        print '[END] function \'generate_token_list\'\n'


#scan = Scanner( file_to_string( 'files/lexers/lua.lex' ) )

#scan.generate_token_list('a = 1 123232323.11212')


scan = Scanner( file_to_string( 'files/lexers/java.lex' ) )

scan.generate_token_list('public void static main () \nint a += 1 123232323.11212')
