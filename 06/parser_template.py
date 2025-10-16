DEBUG = True

class Parser:
    def __init__(self, file):
        if DEBUG:
            print("Initializing Parser...")
        self.file = file                    #Dateiobjekt
        self.raw_lines = file.readlines()   #Speichert die originalen Zeilen der Datei
        self.lines = {}                     #Dictionary f�r die bereinigten Zeilen
        self.symbols = self.predefined_symbols()    #Liste aller Symbole
        self.current_address = 16           #Erste freie Adresse f�r Variable
        self.parse()                        #Starte den Parsing Prozess   

    def print(self):
        print("------- Symbols -------")
        #dein Code hier
        print("------- Lines -------")
        #dein Code hier

    def predefined_symbols(self):
        """
        Vordefinierte Symbole.
        """
        return {'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5,
            'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11,
            'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15, 'LOOP' : 10, 'END' : 23,
            'SCREEN' : 16384, 'KBD' : 24576}
                        
    def parse(self)->None:
        if DEBUG:
            print("Parsing...")
        # 1. Durchlauf
        self.add_labels()
        # 2. Durchlauf
        self.replace_symbols()

    def clean_line(self, line:str)->str|None:
        """
        Bereinigt eine Zeile, indem Leerzeichen und Kommentare entfernt werden.
        Gibt None zur�ck, wenn die Zeile leer oder ein Kommentar ist.
        """
        line = line.replace(" ", "")

        if len(line) == 0 or line.startswith("//"):
            return None
        else:
            return line
    
    def return_type(self, line: str)->str:
        """
        Bestimmt den Typ einer Anweisung.
        Gibt 'A' f�r A-Befehle, 'C' f�r C-Befehle und 'L' f�r Labels zur�ck.
        """
        if line.startswith("@"):
            try:
                if int(line[1:]) <= 24576:
                    x = True
                else:
                    x = False
            except:
                x = False
            finally:
                if x == True or line[1:] in self.symbols.keys():
                    return "A"
                else:
                    return "L"
        else:
            return "C"

    def add_labels(self) -> None:
        """
        Erster Durchlauf: F�gt Labels zur Symboltabelle hinzu und speichert die
        Adressen der Anweisungen.
        """
        line_number = 0
        for line in self.raw_lines:
            cleaned_line = self.clean_line(line)
            if not cleaned_line is None: 
                if self.return_type(line) == "L": #Fehler Wolf! self fehlte
                    self.symbols[line.rstrip("@")] = 16 + line_number
                    line_number += 1

    def replace_symbols(self) -> None:
        """
        Zweiter Durchlauf: Ersetzt Symbole durch Adressen.
        """
        line_number = 0
        for line in self.raw_lines:
            cleaned_line = self.clean_line(line)
            if not cleaned_line is None: #skip comments and empty lines
                type_ = self.return_type(cleaned_line)
                if type_ == 'A': #A-Befehl
                    pass
                    #dein Code hier
                elif type_ == 'C':
                    self.lines[line_number] = cleaned_line
                    line_number += 1
