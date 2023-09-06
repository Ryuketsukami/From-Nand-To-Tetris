

class CodeWriter():

    def __init__(self, output_file_name : str) -> None:
        try:
            with open(output_file_name, "w") as out_file:
                self.static_name = output_file_name[:-3]
                self.file = out_file
        except IOError("something went wrong"):
            pass

    #Writes the command that writes the given code to the outputfile, given that the command is an arithmetic one
    def WriteArithmetic(self, command: str) -> None:
        to_ret = "@SP\nA=M-1\n" # A points to y cell

        if command == 'neg':
            to_ret += 'M=-M\n'

        if command == 'not':
            to_ret += 'M=!M\n'

        if command in ['add', 'sub', 'and', 'or']:
            to_ret += 'D=M\n'
            to_ret += 'A=A-1\n' #A points to x cell

            if command == 'add':
                to_ret += 'M=D+M\n'
            elif command == 'sub':
                to_ret += 'M=M-D\n'
            elif command == 'and':
                to_ret += 'M=D&M\n'
            elif command == 'or':
                to_ret += 'M=D|M\n'

            to_ret += 'D=A+1\n'
            to_ret += '@SP\n'
            to_ret += 'M=D\n'

        if command in ['eq', 'gt', 'lt']:
            to_ret += 'D=M\n'
            to_ret += 'A=A-1\n'
            to_ret += 'D=M-D\n'
            to_ret += '@BEND\n'
            if command == 'eq':
                to_ret += 'D;JEQ\n'
            elif command == 'gt':
                to_ret += 'D;JGT\n'
            elif command == "lt":
                to_ret += 'D;JLT\n'
            to_ret += 'D=0\n'
            to_ret += '@END\n'
            to_ret += '0;JMP\n'
            to_ret += '(BEND)\n'
            to_ret += 'D=-1\n'
            to_ret += '(END)\n'
            to_ret += "@SP\nA=M-1\nA=A-1\nM=D\nD=A+1\n@SP\nM=D\n"

        self.file.write(to_ret)

    #Writes the command that writes the given code to the outputfile, given that the command is a push or pop one
    def WritePushPop(self, command, segment: str, index: int):
        if command == 'C_PUSH':
            to_ret =''
            if segment == 'temp':
                to_ret+= f'@{5+index}\nD=M\n'

                
            to_ret += '@SP\nA=M\nM=D\n@SP\nM=M+1\n'#A points to sp

            

        if command == 'C_POP':
            to_ret = '@SP\nA=M-1\n'#A points to y


        self.file.write( +"\n")

    #close the output file
    def Close(self):
        self.file.close()
        pass