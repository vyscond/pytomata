# -*- coding: iso-8859-1 -*

import automata as dfa

class Scanner(object):

    def __init__(self):

        #------
        
        #self.assigment_operators = ['=']

        #self.math_operators = ['+','-','/','*','%','+=','-=','/=','*=']
        
        #self.relational_operators = ['==','>','>=','<','<=','!=']
        
        #self.logical_operators = ['&&','||','^','!']
        
        #self.reserved_words = [ 'and' , 'break' , 'do' , 'else' , 'elseif' , 'end' , 'false' , 'for' , 'function' , 'if' , 'in' , 'local' , 'nil' , 'not' , 'or' , 'repeat' , 'return' , 'then' , 'true' , 'until' , 'while']
        
        #self.digits = ['1','2','3','4','5','6','7','8','9','0']

        #self.alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        
        #--- dinamic filling
        
        self.assigment_operators = []
        
        self.compound_assignment_operators = []

        self.math_operators = []
        
        self.relational_operators = []
        
        self.logical_operators = []
        
        self.reserved_words = []
        
        self.digits = ['1','2','3','4','5','6','7','8','9','0']

        self.alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        
        self.delimiters = []
        
    def load_lexer_definition_from_file(self,file_path):
        
        lexer_text = (''.join(open(file_path))).strip(' ')
        
        self.fill ( self.search_tag_line('assigment_operators'           , lexer_text) , self.assigment_operators)
        
        self.fill ( self.search_tag_line('compound_assignment_operators' , lexer_text) , self.compound_assignment_operators)
        
        self.fill ( self.search_tag_line('math_operators'                , lexer_text) , self.math_operators)
        
        self.fill ( self.search_tag_line('logical_operators'             , lexer_text) , self.logical_operators)
        
        self.fill ( self.search_tag_line('relational_operators'          , lexer_text) , self.relational_operators)
        
        self.fill ( self.search_tag_line('reserved_words'                , lexer_text) , self.reserved_words)
        
        self.fill ( self.search_tag_line('delimiters'                    , lexer_text) , self.delimiters)
        
        print '+------------------------------------------------------------------------------+'

        for e in self.__dict__.keys(): #--- retorna todas as estruturas declaradas dentro do objeto
            
            #if e in ['dfa_definition' , 'root']: #--- esses dois rotulos não são estruturas lineares
                
            #    continue
                
            print e + ' -> ' , self.__dict__.get(e)[0::1]
            
        
        print '+------------------------------------------------+'
        
        
    def search_tag_line( self , tag , text ):
        
        for l in text.replace('\n','').split(';'):
            
            line_tag = l.split('<-')[0].replace(' ','')

            if line_tag == tag:
                
                return l.split('<-')[1]
   
    def fill(self, values, struct):
        
        for v in values.split(','):

            #--- caracteres especiais

            tmp = v.replace(" ","")

            #if tmp == 'SP':

            #   tmp = ' '

            struct.append(tmp)
            
    #-------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------
    
    def is_integer(self,text):
        
        text = unicode(text)
        
        return True if text.isnumeric() else False
        
        #--- old par method
        
        #~ for c in text:
        #~ 
            #~ if not (c in self.digits) :
                #~ 
                #~ return False
                #~ 
        #~ return True
        
    def is_float(self,text):
        
        text = unicode(text)
        
        return True if text.isdecimal() else False
        
        #--- old par method
        
        #~ if len(text) < 3:
            #~ 
            #~ return False
            #~ 
        #~ dot = False
        #~ 
        #~ for c in text:
        #~ 
            #~ if ( not (c in self.digits) ) and c != '.' :
            #~ 
                #~ return False
                #~ 
            #~ elif c == '.' :
                #~ 
                #~ if dot == False:
                    #~ 
                    #~ dot = True
                #~ 
                #~ else :
                    #~ 
                    #~ return False
        #~ 
        #~ return True

    def is_identifier(self, text):
        
        if text[0].isalpha() :
            
            if text.isalnum() :
                
                return True
        
        return False
        
        #~ for c in text:
#~ 
            #~ if not (c in self.alpha):
#~ 
                #~ return False
#~ 
        #~ return True

    def is_delimiter(self, text):
        
        return ({ ',' : 'comma' , '.' : 'dot' , ';' : 'dot_comma' , '{' : 'open_key' , '}' : 'close_key' , '(' : 'open_parenthesis' , ')' : 'close_parenthesis' , '[' : 'open_bracket' , ']' : 'close_bracket' }).get(text)

    def is_nonterminals(self, text):
        
        print '>>> delimiter ->> '+text
    
        if text in self.relational_operators:
        
            return True
        
        if text in self.logical_operators:
            
            return True
        
        #if text in ['(',')','{','}','[',']',',']:
        if self.is_delimiter(text):
        
            return True
        
        if text in self.math_operators:
        
            return True
        
        if text in self.compound_assignment_operators:
            
            return True
        
        if text in self.assigment_operators:
        
            return True
        
        return False
        

    # 888       888 888    888        d8888 88888888888      8888888 .d8888b.       88888888888 888    888 8888888 .d8888b.  
    # 888   o   888 888    888       d88888     888            888  d88P  Y88b          888     888    888   888  d88P  Y88b 
    # 888  d8b  888 888    888      d88P888     888            888  Y88b.               888     888    888   888  Y88b.      
    # 888 d888b 888 8888888888     d88P 888     888            888   "Y888b.            888     8888888888   888   "Y888b.   
    # 888d88888b888 888    888    d88P  888     888            888      "Y88b.          888     888    888   888      "Y88b. 
    # 88888P Y88888 888    888   d88P   888     888            888        "888          888     888    888   888        "888 
    # 8888P   Y8888 888    888  d8888888888     888            888  Y88b  d88P          888     888    888   888  Y88b  d88P 
    # 888P     Y888 888    888 d88P     888     888          8888888 "Y8888P"           888     888    888 8888888 "Y8888P"  
                                                                                                                       

    def what_is_this(self, text):

        result = None
        
        #--------------------------------------
        print 'reserved words'
        #--------------------------------------
        
        if text in self.reserved_words : 
            
            return 'reserved_word' 

        #--------------------------------------
        print 'operators'
        #--------------------------------------
        
        if text in self.relational_operators : 
            
            return 'relational_operator' 
        
        #--------------------------------------
        
        if text in self.logical_operators :
        
            return 'logical_operator' 

        #-------------------------------------
        print 'assigment'
        #-------------------------------------
        
        if text in self.assigment_operators :
            
            return 'assigment_operator' 
        
        #-------------------------------------
        print 'compound assigment'
        #-------------------------------------
        
        if text in self.compound_assignment_operators :
        
            return 'compound_assigment_operator' 
        
        #-------------------------------------
        print 'math operator'
        #-------------------------------------
        if text in self.math_operators :
        
            return 'math_operator' 
                
        #-------------------------------------
        print 'integer value'
        #-------------------------------------
        if self.is_integer(text) :
        
            return 'integer' 

        #-------------------------------------
        print 'float value'
        #-------------------------------------
        
        if self.is_float(text) :
        
            return 'float' 
        
        #-------------------------------------
        print 'identifier'
        #-------------------------------------
        
        if self.is_identifier(text) :
        
            return 'identifier' 
        
        result = self.is_delimiter(text)
        
        if result:
            
            return result
        
        if text == ')':

            return 'close_parenthese'

        if text == '(':

            return 'open_parenthese'

        if text == ']':

            return 'close_bracket'

        if text == '[':

            return 'open_bracket'

        if text == '}':

            return 'close_key'

        if text == '{':

            return 'open_key'

        if text == ',':

            return 'comma'

        return 'string'
        

    # 88888888888 .d88888b.  888    d8P  8888888888 888b    888 8888888 8888888888P 8888888888 8888888b.  
    #     888    d88P" "Y88b 888   d8P   888        8888b   888   888         d88P  888        888   Y88b 
    #     888    888     888 888  d8P    888        88888b  888   888        d88P   888        888    888 
    #     888    888     888 888d88K     8888888    888Y88b 888   888       d88P    8888888    888   d88P 
    #     888    888     888 8888888b    888        888 Y88b888   888      d88P     888        8888888P"  
    #     888    888     888 888  Y88b   888        888  Y88888   888     d88P      888        888 T88b   
    #     888    Y88b. .d88P 888   Y88b  888        888   Y8888   888    d88P       888        888  T88b  
    #     888     "Y88888P"  888    Y88b 8888888888 888    Y888 8888888 d8888888888 8888888888 888   T88b 

    def tokenizer(self, file_path):

        string = ( ''.join( open(file_path) ) )
        
        buffer = ''
        
        #--- flags
        
        nonterminal = False

        scape = False
        
        squote = False
        
        dquote = False
        
        #--- result tokenized string
        
        string_tokenized = ''
        
        for c in string:
            
            #print 'buffer <'+buffer+'>'
            print 'c = '+c

            #--- whitespace delimiter

            if c == ' ' or c == '\n':
           
                #--- delimiter
                
                if squote == False and dquote == False:
                    
                    #--- verifying buffer content
                    
                    if buffer != '':
                
                        #print 'send to avaliation'
                        #buffer += '\n'
                        print 'buffer <'+buffer+'>'
                        string_tokenized += '\n'+self.what_is_this(buffer)+':'+buffer

                        if c == '\n':

                            string_tokenized += '\neol'

                        buffer = ''
                
                    else :
                 
                        continue
                 
                else:
                    
                    buffer += c
            
            # elif c == '\n':
            #     print 'xD'
            #     string_tokenized += 'eol:'+'eol'+'\n'

            #--- others nonterminals
            #elif self.nonterminals(c) and (not self.nonterminals(buffer)) and buffer != '':
                
                #string_tokenized += '\n'+self.what_is_this(buffer)+':'+buffer

                #buffer = c

            #elif self.nonterminals(c) and self.nonterminals(buffer):

                #buffer += c

            #elif (not self.nonterminals(c)) and self.nonterminals(buffer):
                
                #string_tokenized += '\n'+self.what_is_this(buffer)+':'+buffer

                #buffer = c
            
            #elif c in [',','(',')','{','}','[',']'] :
            elif self.is_nonterminals(c):
                print '>>'
                
                if squote == False and dquote == False :
                    
                    if buffer != '' :
                        
                        print 'buffer <'+buffer+'>'
                        string_tokenized += '\n'+self.what_is_this(buffer)+':'+buffer
                        
                        buffer = ''
                        
                    print 'buffer <'+buffer+'>'
                    string_tokenized += '\n'+self.what_is_this(c)+':'+c
                    
                    continue
                    
                else :
                        
                    buffer += c
                    
    
            elif c == '\\': #---scape sequence
         
                scape = True
                
                continue
            
            #-- the quotes
            
            #--- Single Quote found
            elif c == '\'':
                print 'xD'
                #--- scape was actived?
                if scape == True:
                    
                    buffer += c
                    
                    scape = False
                    
                else :
                    
                    buffer += c #--- put the open/close single quote in the buffer

                    squote = not squote
        
            elif c == '\"':
        
                if scape == True:
                    
                    buffer += c
                    
                    scape = False
                    
                else:
                    
                    buffer += c #--- put the open/close double quote in the buffer

                    dquote = not dquote
                    
        
            else:
        
                buffer += c
        
        return string_tokenized+'\neof'


