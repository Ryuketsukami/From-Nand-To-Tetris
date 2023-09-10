

class CodeWriter():

    def __init__(self, output_file_name : str) -> None:
            self.file = open(output_file_name, "w")
            self.static_name = output_file_name.split('\\')[-1][:-3] #static_name has a '.' at the end
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


    #informs codewriter that there is a new file
    def setFileName(self, fileName : str) -> None:
        self.static_name = fileName.split('\\')[-1][:-3]


    def writeInit(self) -> None:
        self.file.write('@256\nD=A\n@SP\nM=D\n')
        self.writeCall('Sys.Sys.init', 0)
        


    def writeLabel(self, label : str) ->None:
        self.file.write(f'({label})\n')


    def writeGoto(self, label : str) ->None:
        self.file.write(f'@{label}\n0;JMP\n')


    def writeIf(self, label : str)->None:
        self.file.write(f'@SP\nM=M-1\nA=M\nD=M+1\n@{label}\nD;JEQ\n')


    def writeFunction(self, functionName : str, numVars : int)->None:
        self.file.write(f'({self.static_name}{functionName})\n')
        for num in range(numVars):
            self.WritePushPop("C_PUSH", 'constant', 0)
        self.writeReturn()


    def writeCall(self, functionName: str, numArgs : int)->None:
        self.file.write(f'@{self.static_name}{functionName}$ret.{self.id}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n') #push the ret address
        self.file.write(f'@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n') #push the LCL address
        self.file.write(f'@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.file.write(f'@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.file.write(f'@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.file.write(f'@{5+numArgs}\nD=A\n@SP\nD=M-D\n@ARG\nM=D\n') #arg = newarg
        self.file.write(f'@SP\nD=M\n@LCL\nM=D\n') #lcl is new lcl
        self.writeGoto(f'{self.static_name}{functionName}')


    def writeReturn(self)->None:
        self.WritePushPop('C_POP', 'argument', 0) #put the return value into arg 0
        self.file.write('@LCL\nD=M\n@SP\nM=D\n') #SP is now at LCL
        self.WritePushPop('C_POP', 'pointer', 1)
        self.WritePushPop('C_POP', 'pointer', 0)
        self.WritePushPop('C_POP', 'temp', 0) #temp 0 contains the address that arg has to get
        
        self.file.write('@SP\nM=M-1\nA=M\nD=M\n') #D has what LCL has to get AND SP = sp-1
        self.file.write('@LCL\nM=D\n') #LCL has old adress

        self.WritePushPop('C_POP', 'temp', 1) #temp 1 contains the ret address
        self.file.write('@ARG\nD=M\n@SP\nM=D+1\n') #SP is now at the right spot

        self.file.write(f'@{5}\nD=M\n@ARG\nM=D\n') #arg is at the right spot
        self.file.write(f'@{6}\nA=M\n0;JMP\n') #we jamp to the ret addr pay attention if ret add is after the tag

