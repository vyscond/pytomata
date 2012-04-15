
class RegularGrammar(object):

    def __init__(self, file_path):

        self.name = file_path.split('/')[-1].replace('.rg', '')

        self.file_text = ''.join(open(file_path))

        #---------------------

        self.values = []

        self.frequency = ()

    def search_tag_line(self, tag, text):
        
        for l in text.replace('\n','').split(';'):

            line_tag = l.split(':')[0]

            if line_tag == tag

