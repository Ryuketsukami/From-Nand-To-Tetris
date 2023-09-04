import sys
from Parser import Parse
from SymbolTable import SymbolTable
from Code import ToCode

def main():
    parsed_lst = Parse(sys.argv[1])
    st_obj = SymbolTable.MakeSymbolTable(parsed_lst)
    st = st_obj.GetDict()
    coded_lst = ToCode(parsed_lst, st)
    try:   
        with open("my_assembled.out", 'w') as file_to_write:
            for line in coded_lst:
                file_to_write.write(line+'\n')
    except IOError("problem Writing"):
        pass
