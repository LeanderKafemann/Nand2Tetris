import sys
from . import parser_template as p
from . import instructions_template as i

print("--- Skript gestartet ---", flush=True) 

# 1. Prüfen, ob der Dateiname als Argument übergeben wurde
if len(sys.argv) < 2:
    filename = input("Dateipfad angeben: ")
else:# Der Dateiname ist das erste Argument nach dem Skriptnamen
    filename = sys.argv[1]

# Datei öffnen und Fehler abfangen
try:
    with open(filename, 'r') as file:
        
        print(f"--- Parser for '{filename}' ---")
        #2. Erzeuge ein Parser Objekt
        parser = p.Parser(file)
        #Ergebniss des Parsers ausgeben -> Print Methode in parser.py anpassen
        #kann auch auskommentiert werden
        parser.print()

        #3. Erzeuge ein Instructions Objekt
        instructions = i.Instructions(parser)
        #4. Schreibe den Maschinencode in eine .hack Datei
        instructions.write(filename)

except FileNotFoundError:
    # 5. Fehlerbehandlung
    print(f"Error: Die Datei '{filename}' wurde nicht gefunden.")
    sys.exit(1)

print("--- Verarbeitung abgeschlossen ---")