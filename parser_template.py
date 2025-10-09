DEBUG = True

class Parser:
    def __init__(self, file):
        if DEBUG:
            print("Initializing Parser...")
        self.file = file                    #Dateiobjekt
        self.raw_lines = file.readlines()   #Speichert die originalen Zeilen der Datei
        self.lines = {}                     #Dictionary für die bereinigten Zeilen
        self.symbols = self.predefined_symbols()    #Liste aller Symbole
        self.current_address = 16           #Erste freie Adresse für Variable
        self.parse()                        #Starte den Parsing Prozess   

    def print(self):
        print("------- Symbols -------")
        #dein Code hier
        print("------- Lines -------")
        #dein Code hier

    def predefined_symbols(self):
        return {
            'R0': 0,
            'R1': 1,
            'R2': 2,
            #ergänze hier die restlichen vordefinierten Symbole
            }
                        
    def parse(self)->None:
        if DEBUG:
            print("Parsing...")
        # 1. Durchlauf
        self.add_labels()
        # 2. Durchlauf
        self.replace_symbols()

    def clean_line(self, line:str)->str|None:
        ''''
        Bereinigt eine Zeile, indem Leerzeichen und Kommentare entfernt werden.
        Gibt None zurück, wenn die Zeile leer oder ein Kommentar ist.
        '''
        # 1. Entferne Whitespaces
        #dein Code hier

        # 2. Ignoriere Kommentare und leere Zeilen
        #dein Code hier
        return line
    
    def return_type(self, line:str)->str:
        ''''
        Bestimmt den Typ einer Anweisung.
        Gibt 'A' für A-Befehle, 'C' für C-Befehle und 'L' für Labels zurück.
        '''
        return None

    def add_labels(self)->None:
        ''''
        Erster Durchlauf: Fügt Labels zum Symboltabelle hinzu und speichert die
        Adressen der Anweisungen.
        '''
        line_number = 0
        for line in self.raw_lines:
            cleaned_line = self.clean_line(line)
            if not cleaned_line is None: 
                pass
                #dein Code hier
            
    def replace_symbols(self)->None:
        ''''
        Zweiter Durchlauf: Ersetzt Symbole durch Adressen.
        '''
        line_number = 0
        for line in self.raw_lines:
            cleaned_line = self.clean_line(line)
            if not cleaned_line is None: #skip comments and empty lines
                type = self.return_type(cleaned_line)
                if type == 'A': #A-Befehl
                    pass
                    #dein Code hier
                elif type == 'C':
                    self.lines[line_number] = cleaned_line
                    line_number += 1
