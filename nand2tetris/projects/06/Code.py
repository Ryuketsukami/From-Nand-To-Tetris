
CompTable = {
    '0' : '0101010',
    '1' : '0111111',
    '-1' : '0111010',
    'D' : '0001100',
    'A' : '0110000',
    '!D' : '0001101',
    '!A' : '0110001',
    '-D' : '0001111',
    '-A' : '0110011',
    'D+1' : '0011111',
    'A+1' : '0110111',
    'D-1' : '0001110',
    'A-1' : '0110010',
    'D+A' : '0000010',
    'D-A' : '0010011',
    'A-D' : '0000111',
    'D&A' : '0000000',
    'D|A' : '0010101',
    'M' : '1110000',
    '!M' : '1110001',
    '-M' : '1110011',
    'M+1' : '1110111',
    'M-1' : '1110010',
    'D+M' : '1000010',
    'D-M' : '1010011',
    'M-D' : '1000111',
    "D&M" : '1000000',
    'D|M' : '1010101'
}

DestTable = {
    None : '000',
    'M' : '001',
    'D' : '010',
    'MD' : '011',
    'A' : '100',
    'AM' : '101',
    'AD' : '110',
    'AMD' : '111'
}

JumpTable = {
    None : '000',
    'JGT' : '001',
    'JEQ' : '010',
    'JGE' : '011',
    'JLT' : '100',
    'JNE' : '101',
    'JLE' : '110',
    'JMP' : '111'
}





#returns a list of strings
def ToCode(lst, st):
    ret_lst = []
    for line in lst:
        value = 0
        if line.get('addr', -1) != -1:
            addr = line.get('addr')
            if addr in st:
                value = st[addr]
            else:
                value = addr
            value = value[2:]
            counter = 16 - len(value)
            for i in range(counter):
                value = '0' + value
        elif line.get('tag', -1) != -1:
            continue
        else:
            value = '111'
            value = value + CompTable[line['comp']]
            value = value + DestTable[line.get('dest', None)]
            value = value + JumpTable[line.get('jump', None)]
        ret_lst.append(value)
    return ret_lst




            
            

