import sys, os
import parser_template as p
import instructions_template as i

# requires naturalsize
from naturalsize import special_starter

print("--- Skript gestartet ---", flush=True) 
print("Thanks for using EasyAssembler v0.3.0 Copyright LeanderKafemann + NotGhostpro 2025")

# 1. Prüfen, ob der Dateiname als Argument übergeben wurde
if len(sys.argv) < 2:
    filenames = [input("Dateipfad angeben: ")]
    if os.path.isdir(filenames[0]):
        dir_path = filenames[0]
        filenames = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.asm')]
else:# Der Dateiname ist das erste Argument nach dem Skriptnamen
    if os.path.isdir(sys.argv[1]):
        dir_path = sys.argv[1]
        filenames = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.asm')]
    else:
        filenames = [sys.argv[1]]

print("Press Strg+c to cancel printing of to-be-assembled file now.")
print_ = special_starter()

for filename in filenames:
    # Datei öffnen und Fehler abfangen
    try:
        with open(filename, 'r') as file:
        
            print(f"--- Parser for '{filename}' ---")
            #2. Erzeuge ein Parser Objekt
            parser = p.Parser(file)

            #3. Erzeuge ein Instructions Objekt
            instructions = i.Instructions(parser)

            #Ergebniss des Parsers ausgeben -> Print Methode in parser.py anpassen
            #kann auch auskommentiert werden
            if print_:
                instructions.DEBUG = False
                parser.print()

            #4. Schreibe den Maschinencode in eine .hack Datei
            instructions.write(filename)

    except FileNotFoundError:
        # 5. Fehlerbehandlung
        print(f"Error: Die Datei '{filename}' wurde nicht gefunden.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

    print("--- Verarbeitung abgeschlossen ---")
input("Enter drücken zum Beenden...")