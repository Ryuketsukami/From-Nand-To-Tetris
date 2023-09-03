

class SymbolTable():
    def __Init__(self):
        self.st = {
        'R0' : 0,
        'R1' : 1,
        'R2' : 2,
        'R3' : 3,
        'R4' : 4,
        'R5' : 5,
        'R6' : 6,
        'R7' : 7,
        'R8' : 8,
        'R9' : 9,
        'R10' : 10,
        'R11' : 11,
        'R12' : 12,
        'R13' : 13,
        'R14' : 14,
        'R15' : 15,
        'SCREEN' : 16384,
        'KBD' : 24576,
        'SP' : 0,
        'LCL' : 1,
        'ARG' : 2,
        'THIS' : 3,
        'THAT' : 4}

    def Update(self, lst):
        counter = 0
        for i, line in enumerate(lst):
            if line.get('tag', -1) != -1:
                self.st[line.get('tag')] = i - counter
                counter +=1
        counter = 16
        for i, line in enumerate(lst):
            if line.get('addr', -1) != -1:
                word = line.get('addr')
                for letter in word:
                    if ord(letter) > ord('9') or ord(letter) < ord('0'):
                        if self.st.get(word, -1) == -1:
                            self.st[word] = counter
                            counter += 1
                        break

    def MakeSymbolTable(lst):
        st = SymbolTable()
        st.Update(lst)
        return st






