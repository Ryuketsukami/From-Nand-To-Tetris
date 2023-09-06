

import sys
from Parser import Parser
from CodeWriter import CodeWriter

def main():
    parse = Parser(sys.argv[1])
    cw = CodeWriter(sys.argv[1][:-2] + 'asm')
    arg1 = None
    arg2 = None
    while (parse.hasMoreCommands()):
        parse.advance()
        cmd_type = parse.commandType()
        
        if cmd_type != 'C_RETURN':
            arg1 = parse.arg1()
        if cmd_type in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
            arg2 = parse.arg2()
        
        if cmd_type == 'C_ARITHMETIC':
            cw.WriteArithmetic(arg1)
        elif cmd_type in ['C_PUSH', "C_POP"]:
            cw.WritePushPop(cmd_type, arg1, arg2)
    pass

main()
