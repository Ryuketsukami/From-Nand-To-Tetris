import sys
from Parser import Parse
from SymbolTable import *
from Code import ToCode

def main():
    parsed_lst = Parse(sys.argv[1])
    st_obj = SymbolTable.MakeSymbolTable(parsed_lst)
    st = st_obj.GetDict()
    coded_lst = ToCode(parsed_lst, st)
    try:   
        with open("assembled.hack", 'w') as file_to_write:
            file_to_write.write('\n'.join(coded_lst))
    except IOError("problem Writing"):
        pass

main()
