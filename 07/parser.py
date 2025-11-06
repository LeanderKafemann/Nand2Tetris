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
        print(self.symbols)
        print("------- Lines -------")
        print(self.lines)

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
        Gibt None zurück, wenn die Zeile leer oder ein Kommentar ist.
        """
        # Kommentare entfernen (inkl. inline), Zeilenumbruch entfernen und Leerzeichen entfernen
        line = line.split("//", 1)[0].strip()
        line = line.replace(" ", "")
        if len(line) == 0:
            return None
        return line
    
    def return_type(self, line: str)->str:
        """
        Bestimmt den Typ einer Anweisung.
        Gibt 'A' für A-Befehle (z.B. @123 oder @symbol),
        'L' für Labels (z.B. (LOOP)) und 'C' für C-Befehle zurück.
        """
        if line.startswith("@"):
            return "A"
        if line.startswith("(") and line.endswith(")"):
            return "L"
        return "C"

    def add_labels(self) -> None:
        """
        Erster Durchlauf: Fügt Labels zur Symboltabelle hinzu und speichert die
        Adressen der Anweisungen.
        """
        line_number = 0
        for raw in self.raw_lines:
            cleaned_line = self.clean_line(raw)
            if cleaned_line is None:
                continue
            t = self.return_type(cleaned_line)
            if t == "L":
                # Label: (LABEL) -> symbol = LABEL, Adresse = aktuelle Instr.-Adresse
                symbol = cleaned_line[1:-1]
                self.symbols[symbol] = line_number
            else:
                # A- oder C-Befehl erhöht die Instr.-Adresse
                line_number += 1

    def replace_symbols(self) -> None:
        """
        Zweiter Durchlauf: Ersetzt Symbole durch Adressen.
        Speichert bereinigte / ersetzte A- und C-Anweisungen in self.lines mit
        aufsteigender Instr.-Adresse als Schlüssel.
        """
        line_number = 0
        for raw in self.raw_lines:
            cleaned_line = self.clean_line(raw)
            if cleaned_line is None:
                continue
            type_ = self.return_type(cleaned_line)
            if type_ == 'A':  # A-Befehl
                symbol = cleaned_line[1:]
                if symbol.isdigit():
                    address = int(symbol)
                else:
                    if symbol in self.symbols:
                        address = self.symbols[symbol]
                    else:
                        # neue Variable -> erste freie Adresse verwenden
                        address = self.current_address
                        self.symbols[symbol] = address
                        self.current_address += 1
                # Speichere als numerische A-Anweisung (bereinigt)
                self.lines[line_number] = f"@{address}"
                line_number += 1
            elif type_ == 'C':
                self.lines[line_number] = cleaned_line
                line_number += 1