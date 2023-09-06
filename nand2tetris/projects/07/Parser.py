

class Parser():
    def __init__(self, input_file_name : str):
            self.file = open(input_file_name, "r")
            self.current_line = None
            self.ari_table = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']
            self.next_line = self.file.readline()


    #overwrites the next line, use with care
    def hasMoreCommands(self) -> bool:
        if self.next_line == '':
            self.file.close()
            return False
        return True

    def advance(self):
        self.current_line = self.next_line
        self.next_line = self.file.readline()

    def commandType(self):
        cleaned = self.current_line.strip().split('//')[0].strip()
        if cleaned in self.ari_table:
            return 'C_ARITHMETIC'
        elif 'pop' in cleaned and cleaned.index('pop') == 0:
            return 'C_POP'
        elif 'push' in cleaned and cleaned.index('push') == 0:
            return 'C_PUSH'
        #return 'C_LABEL'
        #return 'C_GOTO'
        #return 'C_IF'
        #return 'C_FUNCTION'
        #return 'C_CALL'
        return None




    def arg1(self):
        command = self.commandType()
        if command == 'C_ARITHMETIC':
            return self.current_line.strip().split('/')[0].strip()
        elif command == 'C_POP' or command == 'C_PUSH':
            return self.current_line.strip().split('/')[0].strip().split(' ')[1]
        else:
            return

    def arg2(self):
        command = self.commandType()
        if command == 'C_POP' or command == 'C_PUSH':
            return self.current_line.strip().split('/')[0].strip().split(' ')[2]
        elif command == 'C_FUNCTION':
            return
        elif command == 'C_CALL':
            return
        else:
            return
