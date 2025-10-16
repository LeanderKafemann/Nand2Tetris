import parser_template
Parser = parser_template.Parser

DEBUG = True    #Debug Modus

class Instructions:
    def __init__(self, parser:Parser) -> None:
        self.parser = parser                   #Parser Objekt
        self.instructions = []                 #Liste der Maschinencode Anweisungen
        self.translate()                        #Starte den Übersetzungsprozess

    def translate(self)->None:
        '''
        Übersetzt die bereinigten Zeilen des Parsers in Maschinencode.
        '''
        for num, line in self.parser.lines.items():
            if DEBUG: print(line)
            type = self.parser.return_type(line)
            if type == 'A':
                self.instructions.append(self.assemble_A(line))
            elif type == 'C':
                self.instructions.append(self.assemble_C(line))

    def assemble_A(self, line:str)->str:
        '''
        Übersetzt einen A-Befehl in Maschinencode.
        '''
        # Entferne das @ und wandle die Zahl in eine 15-Bit-Binärzahl um
        value = int(line[1:])
        return '0' + format(value, '015b')

    def assemble_C(self, line:str)->str:
        ''''
        Übersetzt einen C-Befehl in Maschinencode.
        '''
        # Tabellen für comp, dest, jmp
        comp_table = {
            '0':   '101010', '1':   '111111', '-1':  '111010',
            'D':   '001100', 'A':   '110000', '!D':  '001101',
            '!A':  '110001', '-D':  '001111', '-A':  '110011',
            'D+1': '011111', 'A+1': '110111', 'D-1': '001110',
            'A-1': '110010', 'D+A': '000010', 'D-A': '010011',
            'A-D': '000111', 'D&A': '000000', 'D|A': '010101',
        }
        comp_table_M = {k.replace('A','M'):v for k,v in comp_table.items() if 'A' in k}
        comp_table.update({k:v for k,v in comp_table_M.items()})
        dest_table = {
            None:  '000', 'M':   '001', 'D':   '010', 'MD':  '011',
            'A':   '100', 'AM':  '101', 'AD':  '110', 'AMD': '111',
        }
        jmp_table = {
            None:  '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
            'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111',
        }
        # Zerlege die Zeile in dest, comp, jmp
        dest, comp, jmp = None, None, None
        if '=' in line:
            dest, rest = line.split('=')
        else:
            rest = line
        if ';' in rest:
            comp, jmp = rest.split(';')
        else:
            comp = rest
        # a-Bit bestimmen
        a = '1' if 'M' in comp else '0'
        comp_bits = comp_table.get(comp.replace('M','A'), '000000')
        dest_bits = dest_table.get(dest, '000')
        jmp_bits = jmp_table.get(jmp, '000')
        return '111' + a + comp_bits + dest_bits + jmp_bits
           
    def write(self, filename:str)->None:
        full_name = filename.replace('.asm', '.hack')
        with open(full_name, 'w') as file:
            for instruction in self.instructions:
                file.write(instruction + '\n')