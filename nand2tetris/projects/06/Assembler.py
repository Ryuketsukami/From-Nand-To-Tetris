import sys
from Parser import Parse
from SymbolTable import SymbolTable

def main():
    parsed_lst = Parse(sys.argv[1])
    st = SymbolTable.MakeSymbolTable(parsed_lst)
    coded_lst = Something()
    try:   
        with open("my_assembled.out", 'w') as file_to_write:
            for line in coded_lst:
                file_to_write.write(line+'\n')
    except IOError("problem Writing"):
        pass
