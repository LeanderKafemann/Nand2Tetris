import os

import parser_template
Parser = parser_template.Parser

DEBUG = True    #Debug Modus

class Instructions:
    def __init__(self, parser:Parser) -> None:
        self.parser = parser                   # Parser Objekt
        self.instructions = []                 # Liste der Maschinencode Anweisungen
        self.DEBUG = DEBUG                     # Instanz-DEBUG (überschreibbar)
        self.translate()                        # Starte den Übersetzungsprozess

    def translate(self)->None:
        '''
        Übersetzt die bereinigten Zeilen des Parsers in Maschinencode.
        '''
        # sortieren nach Schlüssel, um die Ausgabe-Reihenfolge deterministisch zu halten
        for num in sorted(self.parser.lines.keys()):
            line = self.parser.lines[num]
            if self.DEBUG:
                print(line)
            type_ = self.parser.return_type(line)
            if type_ == 'A':
                self.instructions.append(self.assemble_A(line))
            elif type_ == 'C':
                self.instructions.append(self.assemble_C(line))

    def assemble_A(self, line:str)->str:
        '''
        Übersetzt einen A-Befehl in Maschinencode.
        '''
        # Entferne das @ und wandle die Zahl in eine 15-Bit-Binärzahl um
        try:
            value = int(line[1:])
        except ValueError as e:
            raise ValueError(f"Ungültige A-Anweisung: {line}") from e
        return '0' + format(value, '015b')

    def assemble_C(self, line:str)->str:
        '''
        Übersetzt einen C-Befehl in Maschinencode.
        '''
        # Basis comp-Tabelle für A-Varianten (6 Bits)
        comp_a = {
            '0':   '101010', '1':   '111111', '-1':  '111010',
            'D':   '001100', 'A':   '110000',
            '!D':  '001101', '!A':  '110001',
            '-D':  '001111', '-A':  '110011',
            'D+1': '011111', 'A+1': '110111',
            'D-1': '001110', 'A-1': '110010',
            'D+A': '000010', 'D-A': '010011', 'A-D': '000111',
            'D&A': '000000', 'D|A': '010101',
        }
        # Erzeuge automatisch M-Varianten (gleiche 6 Bits), falls benötigt
        comp_table = dict(comp_a)
        for k, v in list(comp_a.items()):
            if 'A' in k:
                comp_table[k.replace('A','M')] = v

        dest_table = {
            '':    '000', 'M':   '001', 'D':   '010', 'MD':  '011',
            'A':   '100', 'AM':  '101', 'AD':  '110', 'AMD': '111',
        }
        jmp_table = {
            '':    '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
            'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111',
        }

        # Zerlege die Zeile in dest, comp, jmp (maxsplit=1 wichtig)
        dest = ''
        jmp = ''
        if '=' in line:
            dest, rest = line.split('=', 1)
        else:
            rest = line
        if ';' in rest:
            comp, jmp = rest.split(';', 1)
        else:
            comp = rest

        # Normalisiere dest: feste Reihenfolge A, D, M -> liefert z.B. 'AD' statt 'DA'
        dest_norm = ''.join(ch for ch in 'ADM' if ch in dest)

        # Bestimme a-Bit (1 falls M in comp vorkommt)
        a_bit = '1' if 'M' in comp else '0'
        comp_key = comp  # comp enthält bereits A oder M

        comp_bits = comp_table.get(comp_key)
        if comp_bits is None:
            raise ValueError(f"Unbekannter Comp-Wert: '{comp}' in Zeile '{line}'")

        dest_bits = dest_table.get(dest_norm, '000')
        jmp_bits = jmp_table.get(jmp, '000')

        return '111' + a_bit + comp_bits + dest_bits + jmp_bits

    def write(self, filename:str)->None:
        full_name = filename.replace('.asm', '.hack')
        if os.path.exists(full_name):
            print(f"Hack file at {full_name} was overwritten.")
        with open(full_name, 'w') as file:
            for instruction in self.instructions:
                file.write(instruction + '\n')