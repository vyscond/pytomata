import grammyr2 as gf

a = gf.RegularGrammar()

gd_str = gf.file_to_string( 'grfile' )

a.general_definition = gd_str
a.build_nonterminal_token_table()
print a.replace_nonterminals('afd')

