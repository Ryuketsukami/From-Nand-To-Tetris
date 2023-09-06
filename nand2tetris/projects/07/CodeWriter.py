

class CodeWriter():

    def __init__(self, output_file_name : str) -> None:
            self.file = open(output_file_name, "w")
            self.static_name = output_file_name.split('\\')[-1][:-3]
            self.id = 0


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
            to_ret += f'@BEND{self.id}\n'
            if command == 'eq':
                to_ret += 'D;JEQ\n'
            elif command == 'gt':
                to_ret += 'D;JGT\n'
            elif command == "lt":
                to_ret += 'D;JLT\n'
            to_ret += 'D=0\n'
            to_ret += f'@END{self.id}\n'
            to_ret += '0;JMP\n'
            to_ret += f'(BEND{self.id})\n'
            to_ret += 'D=-1\n'
            to_ret += f'(END{self.id})\n'
            to_ret += "@SP\nA=M-1\nA=A-1\nM=D\nD=A+1\n@SP\nM=D\n"
        self.id+=1
        self.file.write(to_ret)

    #Writes the command that writes the given code to the outputfile, given that the command is a push or pop one
    def WritePushPop(self, command, segment: str, index: int):
        to_ret =''
        if command == 'C_PUSH':
            if segment == 'temp':
                to_ret+= f'@{5+int(index)}\nD=M\n'
            if segment == 'local':
                to_ret+= f'@{index}\nD=A\n@LCL\nA=D+M\nD=M\n'
            if segment == 'argument':
                to_ret+= f'@{index}\nD=A\n@ARG\nA=D+M\nD=M\n'
            if segment == 'this':
                to_ret+= f'@{index}\nD=A\n@THIS\nA=D+M\nD=M\n'
            if segment == 'that':
                to_ret+= f'@{index}\nD=A\n@THAT\nA=D+M\nD=M\n'
            if segment == 'pointer' and index == '0':
                to_ret += '@THIS\nD=M\n'
            if segment == 'pointer' and index == '1':
                to_ret += '@THAT\nD=M\n'
            if segment == 'constant':
                to_ret+= f'@{index}\nD=A\n'
            if segment == 'static':
                to_ret += f'@{self.static_name}{index}\nD=M\n'                
            to_ret += '@SP\nA=M\nM=D\n@SP\nM=M+1\n'#A points to sp

        if command == 'C_POP':
            if segment == 'temp':
                to_ret+= f'@SP\nA=M-1\nD=M\n@{5+int(index)}\nM=D\n'
            if segment == 'local':
                to_ret+= f'@{index}\nD=A\n@LCL\nD=D+M\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R13\nA=M\nM=D\n'
            if segment == 'argument':
                to_ret+= f'@{index}\nD=A\n@ARG\nD=D+M\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R13\nA=M\nM=D\n'
            if segment == 'this':
                to_ret+= f'@{index}\nD=A\n@THIS\nD=D+M\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R13\nA=M\nM=D\n'
            if segment == 'that':
                to_ret+= f'@{index}\nD=A\n@THAT\nD=D+M\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R13\nA=M\nM=D\n'
            if segment == 'pointer' and index == '0':
                to_ret += '@SP\nA=M-1\nD=M\n@THIS\nM=D\n'
            if segment == 'pointer' and index == '1':
                to_ret += '@SP\nA=M-1\nD=M\n@THAT\nM=D\n'
            if segment == 'static':
                to_ret += f'@SP\nA=M-1\nD=M\n@{self.static_name}{index}\nM=D\n' 
            to_ret += '@SP\nM=M-1\n'

        self.file.write(to_ret)

    #close the output file
    def Close(self):
        self.file.close()
        pass