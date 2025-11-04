import os.path
import parser_template
import os

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
        # Vollständige comp-Tabelle (6 Bits) für A- und M-Varianten
        comp_table = {
            '0':   '101010', '1':   '111111', '-1':  '111010',
            'D':   '001100', 'A':   '110000', 'M':   '110000',
            '!D':  '001101', '!A':  '110001', '!M':  '110001',
            '-D':  '001111', '-A':  '110011', '-M':  '110011',
            'D+1': '011111', 'A+1': '110111', 'M+1': '110111',
            'D-1': '001110', 'A-1': '110010', 'M-1': '110010',
            'D+A': '000010', 'D+M': '000010',
            'D-A': '010011', 'D-M': '010011',
            'A-D': '000111', 'M-D': '000111',
            'D&A': '000000', 'D&M': '000000',
            'D|A': '010101', 'D|M': '010101',
        }

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

        # dest normalisieren (Beliebige Reihenfolge -> AMD-Reihenfolge)
        if dest:
            dest_norm = ''.join([ch for ch in 'ADM' if ch in dest])
        else:
            dest_norm = ''

        # a-Bit bestimmen (1 wenn M in comp verwendet wird)
        a_bit = '1' if 'M' in comp else '0'
        comp_key = comp
        # Falls M vorhanden, ersetzen wir 'M' nicht, weil Tabelle enthält M-Versionen
        comp_bits = comp_table.get(comp_key)
        if comp_bits is None:
            raise ValueError(f"Unbekannter Comp-Wert: {comp}")

        dest_bits = dest_table.get(dest_norm, '000')
        jmp_bits = jmp_table.get(jmp, '000')

        return '111' + a_bit + comp_bits + dest_bits + jmp_bits
           
    def write(self, filename:str)->None:
        full_name = filename.replace('.asm', '.hack')
        if os.path.exists(full_name):
            print(f"Hack file {full_name} was overwritten.")
        with open(full_name, 'w') as file:
            for instruction in self.instructions:
                file.write(instruction + '\n')