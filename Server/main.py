from PyWSGIRef import *
from typing import *

__version__ = "1.0.0"
APP_NAME = "Nand2Tetris Server"

BETA.enable()

addSchablone("main", loadFromFile("./templates/main.pyhtml"))

def main(path: str, fs: FieldStorage):
    match path:
        case "/main":
            return SCHABLONEN["main"].decodedContext(globals())
        case "/assembler":
            return "Not ready..."
        case "/translateASM":
            return "Not ready..."
        case "/vmTranslator":
            return "Not ready..."
        case "/translateVM":
            return "Not ready..."
        case "/stats":
            return STATS.export_stats()
        case "/" | _:
            "Not found..."
app = makeApplicationObject(main, advanced=True, getStats=True)

if __name__ == "__main__":
    server = setUpServer(app)
    print("Serving...")
    server.serve_forever()