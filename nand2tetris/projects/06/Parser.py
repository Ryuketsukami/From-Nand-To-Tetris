

def Parse(file_name):
    try:
        with open(file_name, 'r') as in_file:
            lines = [element.split('/')[0].strip() for element in in_file.readlines() if len(element.split('/')[0].strip()) > 0]
            lines = [line for line in lines if line[0] != '/']
            for i, line in enumerate(lines):
                temp_dict = {}
                temp_lst = []
                if line[0] == '@':
                    temp_dict['addr'] = line[1:]
                elif line[0] == '(':
                    temp_dict['tag'] = line[1:-1]
                else:
                    if line.count('=') > 0:
                        temp_lst = line.split('=')
                        temp_dict['dest'] = temp_lst[0]
                        temp_dict['comp'] = temp_lst[1]
                    if line.count(';') > 0:
                        temp_lst = line.split(';')
                        temp_dict['jump'] = temp_lst[-1]
                        temp_dict['comp'] = temp_lst[-2]
                lines[i] = temp_dict
            return lines
    except IOError("failed to load file"):
        return []