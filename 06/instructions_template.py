from parser import Parser

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
        # ersetze mit deinem Code
        return None
    
    def assemble_C(self, line:str)->str:
        ''''
        Übersetzt einen C-Befehl in Maschinencode.
        Hinweise:
        '''
        c_str = '111'

        if '=' in line:
            dest, rest = line.split('=')
        else:
            #dein Code hier
            pass
        if ';' in rest:
            #dein Code hier
            pass
        else:
            #dein Code hier
            pass

        #hier verwenden wir einen elagenten Weg, 
        #um dest in Binärwerte umzuwandeln:
        # 7 = 111
        # 6 = 110
        # usw.
        dest_val = 0
        if not dest is None:
            if "A" in dest:
                dest_val += 4
            if "D" in dest:
                #dein Code hier
                pass
        # umwandeln von in 3-Bit Binärstring    
        dest_str = format(dest_val, '03b')

        jmp_str = '000'
        if not jmp is None:
            if jmp == "JGT":
                jmp_str = '001'
            #dein Code hier

        a_str = '0'  # a=0 for A, a=1 for M
        comp_str = '000000'
        if 'M'in comp:
            a_str = '1'
            comp = comp.replace('M', 'A')  
        if comp == "0":
            comp_str = '101010'
        elif comp == "1":
            #dein Code hier
            pass
        else:
            raise ValueError(f"Unbekannter Comp-Wert: {comp}") 
    
        return None
           
    def write(self, filename:str)->None:
        full_name = filename.replace('.asm', '.hack')
        with open(full_name, 'w') as file:
            for instruction in self.instructions:
                file.write(instruction + '\n')