

import sys
from Parser import *

def main():
    parsed_lst = Parse(sys.argv[1])

    try:   
        with open(sys.argv[1][:-2] + 'asm', 'w') as file_to_write:
            file_to_write.write('\n'.join())
    except IOError("problem Writing"):
        pass

main()
