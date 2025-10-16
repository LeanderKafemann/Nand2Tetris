import sys, os
import parser_template as p
import instructions_template as i

print("--- Skript gestartet ---", flush=True) 

# 1. Prüfen, ob der Dateiname als Argument übergeben wurde
if len(sys.argv) < 2:
    filenames = [input("Dateipfad angeben: ")]
else:# Der Dateiname ist das erste Argument nach dem Skriptnamen
    if os.path.isdir(sys.arvv[1]):
        dir_path = sys.argv[1]
        filenames = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.asm')]
    else:
        filenames = [sys.argv[1]]

for filename in filenames:
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