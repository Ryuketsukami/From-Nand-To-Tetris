

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
        elif '(' in cleaned and ')' in cleaned and cleaned.index('(') == 0:
            return 'C_LABEL'
        elif 'goto' in cleaned and cleaned.index('goto') == 0:
            return 'C_GOTO'
        elif 'if-goto' in cleaned and cleaned.index('if-goto') == 0:
            return 'C_IF'
        elif 'function' in cleaned and cleaned.index('function') == 0:
            return 'C_FUNCTION'
        elif 'call' in cleaned and cleaned.index('call') == 0:
            return 'C_CALL'
        return None




    def arg1(self):
        command = self.commandType()
        if command == None:
            return
        elif command == 'C_ARITHMETIC':
            return self.current_line.strip().split('/')[0].strip()
        else:
            return self.current_line.strip().split('/')[0].strip().split(' ')[1]

    def arg2(self):
        command = self.commandType()
        if command == 'C_POP' or command == 'C_PUSH' or command == "C_FUNCTION" or command == "C_CALL":
            return self.current_line.strip().split('/')[0].strip().split(' ')[2]
        else:
            return
