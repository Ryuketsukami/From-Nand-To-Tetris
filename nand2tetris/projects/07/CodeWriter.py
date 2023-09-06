

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

        self.file.write( +"\n")

    #Writes the command that writes the given code to the outputfile, given that the command is a push or pop one
    def WritePushPop(self, command, segment: str, index: int):
        if command == 'C_PUSH':

        if command == 'C_POP':


        self.file.write( +"\n")

    #close the output file
    def Close(self):
        self.file.close()
        pass