import automata as dfa

class Scanner(object):

    def __init__(self):

        #------
        
        self.allocation_operators = ['=']

        self.math_operators = ['+','-','/','*','%','+=','-=','/=','*=']
        
        self.relational_operators = ['==','>','>=','<','<=','!=']
        
        self.logical_operators = ['&&','||','^','!']
        
        self.reserved_words = [ 'and' , 'break' , 'do' , 'else' , 'elseif' , 'end' , 'false' , 'for' , 'function' , 'if' , 'in' , 'local' , 'nil' , 'not' , 'or' , 'repeat' , 'return' , 'then' , 'true' , 'until' , 'while']
        
        self.digits = ['1','2','3','4','5','6','7','8','9','0']

        self.alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

    def integer(self,text):

        for c in text:

            if not (c in self.digits) :

                return False

        return 'integer'

    def float(self,text):

        dot = False

        for c in text:

            if not (c in self.digits) :

                return False

        return 'float'

    def identifier(self, text):

        for c in text:

            if not (c in self.alpha):

                return False

        return 'identifier'

    def nonterminals(self, text):

        if text in self.relational_operators:

            return True

        if text in self.logical_operators:
            
            return True

        if text in ['(',')','{','}','[',']',',']:

            return True

        if text in self.math_operators:

            return True

        if text in self.allocation_operators:

            return True

        return False

    #888       888 888    888        d8888 88888888888      8888888 .d8888b.       88888888888 888    888 8888888 .d8888b.  
    #888   o   888 888    888       d88888     888            888  d88P  Y88b          888     888    888   888  d88P  Y88b 
    #888  d8b  888 888    888      d88P888     888            888  Y88b.               888     888    888   888  Y88b.      
    #888 d888b 888 8888888888     d88P 888     888            888   "Y888b.            888     8888888888   888   "Y888b.   
    #888d88888b888 888    888    d88P  888     888            888      "Y88b.          888     888    888   888      "Y88b. 
    #88888P Y88888 888    888   d88P   888     888            888        "888          888     888    888   888        "888 
    #8888P   Y8888 888    888  d8888888888     888            888  Y88b  d88P          888     888    888   888  Y88b  d88P 
    #888P     Y888 888    888 d88P     888     888          8888888 "Y8888P"           888     888    888 8888888 "Y8888P"  
                                                                                                                       

    def what_is_this(self, text):

        #print 'what is <'+text+'>'

        #print '[begin avaliation]'

        result = None
        
        #--- reserved words
        #--------------------------------------
        result =  text in self.reserved_words
        
        #print '[as reserved_word]'

        if result:
            #print '[ok]'
            return 'reserved_word:'+text

        #print '[fail]'
        #--------------------------------------

        #--- operator
        #--------------------------------------
        #print '[as relational_operator]'

        result = text in self.relational_operators
        
        if result:

            #print '[ok]'    
        
            return 'relational_operator'

        #print '[fail]'
        
        #--------------------------------------

        #print '[as logical_operator]'
        
        result = text in self.logical_operators
        
        if result:

            #print '[ok]'

            return 'logical_operator'

        #print '[fail]'

        #-------------------------------------

        #print '[as atribution_operator]'

        result = text in self.allocation_operators
        
        if result:

            #print '[ok]'

            return 'allocation_operator'

        #print '[fail]'

        #-------------------------------------
        result = self.integer(text)
        
        if result:
            
            return result
        
        #-------------------------------------

        # result = self.float(text)
        
        # if result:
            
        #     return result
        
        #-------------------------------------        

        result = text in self.math_operators

        if result:
            
            return 'math_operator'

        #-------------------------------------

        result = self.identifier(text)

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
        

    #88888888888 .d88888b.  888    d8P  8888888888 888b    888 8888888 8888888888P 8888888888 8888888b.  
    #    888    d88P" "Y88b 888   d8P   888        8888b   888   888         d88P  888        888   Y88b 
    #    888    888     888 888  d8P    888        88888b  888   888        d88P   888        888    888 
    #    888    888     888 888d88K     8888888    888Y88b 888   888       d88P    8888888    888   d88P 
    #    888    888     888 8888888b    888        888 Y88b888   888      d88P     888        8888888P"  
    #    888    888     888 888  Y88b   888        888  Y88888   888     d88P      888        888 T88b   
    #    888    Y88b. .d88P 888   Y88b  888        888   Y8888   888    d88P       888        888  T88b  
    #    888     "Y88888P"  888    Y88b 8888888888 888    Y888 8888888 d8888888888 8888888888 888   T88b 

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
            
            print 'buffer <'+buffer+'>'
            print 'c = '+c

            #--- whitespace delimiter

            if c == ' ' or c == '\n':
           
                #--- delimiter
                
                if squote == False and dquote == False:
                    
                    #--- verifying buffer content
                    
                    if buffer != '':
                
                        #print 'send to avaliation'
                        #buffer += '\n'
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
            
            elif c in [',','(',')','{','}','[',']'] :
                print '>>'
                
                if not (squote and dquote) :
                    
                    if buffer != '' :
                        
                        string_tokenized += '\n'+self.what_is_this(buffer)+':'+buffer
                        
                        buffer = ''
                        
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
                    
                    #buffer += c #--- put the open/close double quote in the buffer

                    dquote = not dquote
                    
        
            else:
        
                buffer += c
        
        return string_tokenized+'\neof'


