'''
Created on Feb 21, 2012

@author: abara
'''

def h_line(size, flag):
    
    if flag == 0:
        
        return  ('+-'+('-'*size)+'-')
    
    else:
        
        return  ('+-'+('-'*size)+'-+')

def txt_block(size, text, flag):
        
    dif = size - len(text)
    
    #even and odds
    
    tmp = '| '
    
    if dif % 2 != 0:

        right_spc = dif/2
        
        left_spc  = (dif/2) + 1
        
        tmp += (' ' * right_spc) + text + (' ' * left_spc)
        
    else:
        
        spc = dif / 2
        
        tmp += (' ' * spc) + text + (' ' * spc)
    
    
    if flag == 0:
        
        return (tmp+(' '))
     
    else:
         
        return (tmp+(' |'))

#    if (dif % 2.0) != 0.0:
#        
#        tmp += (' ' * int(border)) + text + (' ' * (int(border) ))
#    
#    else:
#        
#        tmp += (' ' * int(border)) + text + (' ' * int(border)) 
#        
#    if flag == 0:
#        
#        return tmp+(' ')
#     
#    else:
#         
#        return tmp+(' |')

def populate(size):
    
    return [0]*size

def print_table(table_headers,table_tuple_content):
    
    #--- verificar se as tuplas carregadas na table_tuple_content estao sincronizadas com q qtdd de headers
    for t in table_tuple_content:
        
        if len(table_headers) != len(t):

            return
    
    #print '[sync]'
    #---------------------------------------------------------------------------------------------
    
    BIG_TEXT = populate(len(table_headers))
    
    #--- descobrindo qual o maior texto em cada coluna --------------------------------------------------
    for title in table_headers:
        
        column_index = (table_headers.index(title))
        
        #print column_index
        
        if len(title) > BIG_TEXT[column_index]:
            
            BIG_TEXT[column_index] = len(title)
        
        for content in table_tuple_content:
            
            if len(content[column_index]) > BIG_TEXT[column_index]:
                
                BIG_TEXT[column_index] = len(content[column_index])
                
                continue
            
    print BIG_TEXT
    
    #---------------------------------------------------------------------------------------------
    
    
    #--- Formatando as linhas horizontais ---------------------------------------------------------------
    line_template = ""
    
    for i in range(0, len(BIG_TEXT)):
        
        if i == len(BIG_TEXT) - 1:
            
            flag = 1
            
        else:
            
            flag = 0
            
        line_template += h_line(BIG_TEXT[i], flag)

# old lines for formatting H lines
#    for size in BIG_TEXT:
#        
#        if BIG_TEXT.index(size) == len(BIG_TEXT) - 1:  
#            
#            flag = 1
#        
#        else:
#            
#            flag = 0 
#            
#        line_template += h_line(size, flag)
        
    #print line_template
        
    #--- configurando os cabecalhos ----------------------------------------------------------------------
    
    headers_template = ""
    
    for i in range(0, len(BIG_TEXT)):
        
        if i == len(BIG_TEXT) - 1:
            
            flag = 1
            
        else:
            
            flag = 0
            
            
        print BIG_TEXT[i]
        print table_headers[i]
        headers_template += txt_block(BIG_TEXT[i], table_headers[i], flag)

# old line for
#
#    for size in BIG_TEXT:
#        
#        index = BIG_TEXT.index(size)
#        
#        if index == len(BIG_TEXT) - 1:
#        
#            flag = 1
#        
#        else:
#            
#            flag = 0
#            
#        print index
#        print table_headers[index]
#        headers_template += txt_block(size, table_headers[index], flag)
        
    
    #print headers_template
    
    #-----------------------------------------------------------------------------------------------------
    
    
    #--- configurando o conteudo
    
    content_template = line_template +'\n'

    for content_tuple in table_tuple_content:
        
        for i in range(0, len(BIG_TEXT)):
        
            if i == len(BIG_TEXT) - 1:
                
                flag = 1
                
            else:
                
                flag = 0
            
            content_template += txt_block(BIG_TEXT[i], content_tuple[i], flag)
        
        content_template += '\n'+line_template +'\n'    
    
    
# old line for
#   
#    for content_tuple in table_tuple_content:
#        
#        for size in BIG_TEXT:
#            
#            index = BIG_TEXT.index(size)
#            
#            if index == len(BIG_TEXT) - 1:
#        
#                flag = 1
#        
#            else:
#            
#                flag = 0
#            
#            content_template += txt_block(size, content_tuple[index], flag)
#        
#        content_template += '\n'+line_template +'\n'
        
    #print content_template
        
    return line_template+'\n'+headers_template+'\n'+content_template
    
#        for t in table_tuple_content[j]:
#            
#            print t
#            
#            if len(t) > BIG_TEXT[j]:
#                    
#                BIG_TEXT[j] = len(t)
#                    
#        print BIG_TEXT
#        
#        lines = ""
#        
#        for i in range(0, len(table_headers)):
#            
#            if i == len(table_headers) - 1:
#                
#                lines += h_line(BIG_TEXT[i], 1)
#                
#            else:
#                
#                lines += h_line(BIG_TEXT[i], 0)
#                
#        headers = ""
#        
#        #--- concatenando os headers
#        for i in range(0, len(table_headers)):
#            
#            print table_headers[i]
#            print BIG_TEXT[i]
#            
#            if i == len(table_headers) - 1:
#                
#                headers += (txt_block(BIG_TEXT[i], table_headers[i], 1))
#                
#            else:
#                
#                headers += (txt_block(BIG_TEXT[i], table_headers[i], 0))
#        
#        tupless = populate(len(table_tuple_content))
#        
#        for i in range(0, len(table_tuple_content)):
#            
#            tmp = ''
#            
#            for txt in table_tuple_content[i]:
#                
#                if table_tuple_content[i].column_index(txt) == len(txt) - 1:
#                    
#                    flag = 1
#                
#                else:
#                
#                    flag = 0
#                    
#                tmp += (txt_block(BIG_TEXT[table_tuple_content[i].column_index(txt)], txt, flag))
#                    
#                tupless[i] = tmp
#        
#        
#        final_text = ""
#        
#        final_text += lines+"\n"+headers+"\n" +lines
#        
#        for x in tupless:
#            
#            final_text += "\n"+x+"\n"+lines            
#        
#        print final_text
            
            