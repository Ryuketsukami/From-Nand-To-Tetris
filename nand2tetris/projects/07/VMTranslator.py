import sys
import os
from Parser import Parser
from CodeWriter import CodeWriter


#function that takes a directory or tile and returns a list with all the names of the files inside of it
def MakeDirList(dir_or_file : str):
    file_name = ''
    file_paths = []
    file_names = []
    ret_lst = []
    is_dir = False
    if '.vm' in dir_or_file and dir_or_file[-3:] == '.vm':
        file_name = dir_or_file #filename with a path
    else:
        is_dir = True
        file_names = os.listdir(dir_or_file)
        for file in file_names:
            if '.vm' in file and file[-3:] == '.vm':
                file_paths.append(os.path.join(dir_or_file, file))
    if len(file_name) > 0:
        file_paths.append(file_name)
    ret_lst.append(is_dir)
    ret_lst.append(file_paths)
    return ret_lst


def FindOutputName(dir_lst):
    if dir_lst[0] == 0:
        return dir_lst[1][0][:-2] + 'asm'
    else:
        return dir_lst[1][0].split(os.sep)[:-1].join(os.sep) + '.asm'

def DealWithFile(file_path : str, cw):

    parse = Parser(file_path)
    arg1 = None
    arg2 = None
    while (parse.hasMoreCommands()):
        parse.advance()
        cmd_type = parse.commandType()
        if cmd_type == None:
            continue
        if cmd_type != 'C_RETURN':
            arg1 = parse.arg1()
        if cmd_type in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
            arg2 = parse.arg2()
        
        if cmd_type == 'C_ARITHMETIC':
            cw.WriteArithmetic(arg1)
        elif cmd_type in ['C_PUSH', "C_POP"]:
            cw.WritePushPop(cmd_type, arg1, arg2)
    cw.Close()



def main():
    dir_list = MakeDirList(sys.argv[1])
    out_name = FindOutputName(dir_list)

    cw = CodeWriter(out_name) #dir_list[1][i] when i =0 has the first path+filename.asm
    #bootstrap needs to be added here.

    for path in dir_list[1]:
        DealWithFile(path, cw)
    pass
    
    
main()


# import sys
# import os
# from Parser import Parser
# from CodeWriter import CodeWriter

# def main():
#     parse = Parser(sys.argv[1])
#     cw = CodeWriter(sys.argv[1][:-2] + 'asm')
#     arg1 = None
#     arg2 = None
#     while (parse.hasMoreCommands()):
#         parse.advance()
#         cmd_type = parse.commandType()
#         if cmd_type == None:
#             continue
#         if cmd_type != 'C_RETURN':
#             arg1 = parse.arg1()
#         if cmd_type in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
#             arg2 = parse.arg2()
        
#         if cmd_type == 'C_ARITHMETIC':
#             cw.WriteArithmetic(arg1)
#         elif cmd_type in ['C_PUSH', "C_POP"]:
#             cw.WritePushPop(cmd_type, arg1, arg2)
#     cw.Close()

# main()
