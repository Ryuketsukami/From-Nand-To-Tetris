

class CodeWriter():

    def __init__(self, output_file_name : str) -> None:
            self.file = open(output_file_name, "w")
            self.static_name = output_file_name.split('\\')[-1][:-4] #static_name has a '.' at the end
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
                to_ret += 'D;JEQ\n' #jump if true
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
            to_ret += "@SP\nM=M-1\nA=M-1\nM=D\n"
            self.id+=1
        self.file.write(to_ret)

    #Writes the command that writes the given code to the outputfile, given that the command is a push or pop one
    def WritePushPop(self, command, segment: str, ind: int):
        index = int(ind)
        to_ret =''
        if command == 'C_PUSH':
            if segment == 'temp':
                to_ret+= f'@{5+int(index)}\nD=M\n'
            elif segment == 'local':
                to_ret+= f'@{index}\nD=A\n@LCL\nA=D+M\nD=M\n'
            elif segment == 'argument':
                to_ret+= f'@{index}\nD=A\n@ARG\nA=D+M\nD=M\n'
            elif segment == 'this':
                to_ret+= f'@{index}\nD=A\n@THIS\nA=D+M\nD=M\n'
            elif segment == 'that':
                to_ret+= f'@{index}\nD=A\n@THAT\nA=D+M\nD=M\n'
            elif segment == 'pointer' and index == 0:
                to_ret += '@THIS\nD=M\n'
            elif segment == 'pointer' and index == 1:
                to_ret += '@THAT\nD=M\n'
            elif segment == 'constant':
                to_ret+= f'@{index}\nD=A\n'
            elif segment == 'static':
                to_ret += f'@{self.static_name}.{index}\nD=M\n'            
            to_ret += '@SP\nA=M\nM=D\n@SP\nM=M+1\n'#A points to sp

        if command == 'C_POP':
            if segment == 'temp':
                to_ret+= f'@SP\nA=M-1\nD=M\n@{5+int(index)}\nM=D\n'
            elif segment == 'local':
                to_ret+= f'@{index}\nD=A\n@LCL\nD=D+M\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R13\nA=M\nM=D\n'
            elif segment == 'argument':
                to_ret+= f'@{index}\nD=A\n@ARG\nD=D+M\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R13\nA=M\nM=D\n'
            elif segment == 'this':
                to_ret+= f'@{index}\nD=A\n@THIS\nD=D+M\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R13\nA=M\nM=D\n'
            elif segment == 'that':
                to_ret+= f'@{index}\nD=A\n@THAT\nD=D+M\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R13\nA=M\nM=D\n'
            elif segment == 'pointer' and index == 0:
                to_ret += '@SP\nA=M-1\nD=M\n@THIS\nM=D\n'
            elif segment == 'pointer' and index == 1:
                to_ret += '@SP\nA=M-1\nD=M\n@THAT\nM=D\n'
            elif segment == 'static':
                to_ret += f'@SP\nA=M-1\nD=M\n@{self.static_name}.{index}\nM=D\n'  
            to_ret += '@SP\nM=M-1\n'

        self.file.write(to_ret)


    #close the output file
    def Close(self):
        self.file.close()
        pass


    #informs codewriter that there is a new file
    def setFileName(self, fileName : str) -> None:
        self.static_name = fileName.split('\\')[-1][:-3]


    def getFileName(self):
        return self.static_name


    def writeInit(self) -> None:
        self.file.write('@256\nD=A\n@SP\nM=D\n')
        self.writeCall('Sys.init', 0)
        


    def writeLabel(self, label : str) ->None:
        self.file.write(f'({label})\n')


    def writeGoto(self, label : str) ->None:
        self.file.write(f'@{label}\n0;JMP\n')


    def writeIf(self, label : str)->None:
        #M contains -1 if true and 0 if false (but thats only for eq and shit)
        self.file.write(f'@SP\nM=M-1\nA=M\nD=M\n@{label}\nD;JNE\n')


    def writeFunction(self, functionName : str, numVars : int)->None:
        self.file.write(f'({functionName})\n')
        for num in range(int(numVars)):
            self.WritePushPop("C_PUSH", 'constant', 0)
        


    def writeCall(self, functionName: str, numArgs : int)->None: #this might need some fixing
        curr_id = self.id
        self.id+=1
        self.file.write(f'@{functionName}$ret.{curr_id}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n') #return adress(the number) goes to current stack place, stack advances
        self.file.write(f'@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n') #push the LCL address
        self.file.write(f'@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.file.write(f'@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.file.write(f'@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.file.write(f'@{5+int(numArgs)}\nD=A\n@SP\nD=M-D\n@ARG\nM=D\n') #arg = newarg
        self.file.write(f'@SP\nD=M\n@LCL\nM=D\n') #lcl is new lcl
        self.writeGoto(f'{functionName}')
        self.file.write(f'({functionName}$ret.{curr_id})\n')


    def writeReturn(self)->None:
        self.file.write('@5\nD=A\n@LCL\nA=M-D\nD=M\n@R13\nM=D\n') #save the return addr in R13
        self.file.write('@SP\nA=M-1\nD=M\n@ARG\nA=M\nM=D\n') #put the return value into arg 0
        self.file.write('@LCL\nD=M\n@SP\nM=D\n') #SP is now at LCL
        self.WritePushPop('C_POP', 'pointer', 1) #pop that
        self.WritePushPop('C_POP', 'pointer', 0) #pop this
        self.WritePushPop('C_POP', 'temp', 0) #temp 0 contains the address that arg has to get
        
        self.file.write('@SP\nM=M-1\nA=M\nD=M\n') #D has what LCL has to get AND SP = sp-1
        self.file.write('@LCL\nM=D\n') #LCL has old adress

        self.file.write('@ARG\nD=M\n@SP\nM=D+1\n') #SP is now at the right spot #########################we edited so the sp at the end is where the arg is

        self.file.write(f'@{5}\nD=M\n@ARG\nM=D\n') #arg is at the right spot
        self.file.write(f'@R13\nA=M\n0;JMP\n') #we jamp to the ret addr pay attention if ret add is after the tag-----------------------important or A=M+1

