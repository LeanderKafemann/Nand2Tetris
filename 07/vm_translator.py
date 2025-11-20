"""
VM -> Hack ASM Translator (Projekt 7)
Struktur orientiert an bestehenden Dateien (parser/instructions/translator).
Erzeugt pro .vm Datei eine .asm Datei im selben Verzeichnis.
"""
import sys
import os
import itertools
from typing import TextIO, Optional

DEBUG = False

# Parser ---------------------------------------------------------------------
C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"

class VMParser:
    def __init__(self, file: TextIO) -> None:
        self._lines = file.readlines()
        self._index = 0
        self.current_command: Optional[str] = None

    def _clean(self, raw: str) -> Optional[str]:
        line = raw.split("//", 1)[0].strip()
        if not line:
            return None
        return line

    def has_more_commands(self) -> bool:
        i = self._index
        while i < len(self._lines):
            if self._clean(self._lines[i]) is not None:
                return True
            i += 1
        return False

    def advance(self) -> None:
        while self._index < len(self._lines):
            cleaned = self._clean(self._lines[self._index])
            self._index += 1
            if cleaned is not None:
                self.current_command = cleaned
                return
        self.current_command = None

    def command_type(self) -> Optional[str]:
        if self.current_command is None:
            return None
        parts = self.current_command.split()
        cmd = parts[0]
        if cmd == "push":
            return C_PUSH
        if cmd == "pop":
            return C_POP
        return C_ARITHMETIC

    def arg1(self) -> Optional[str]:
        if self.current_command is None:
            return None
        t = self.command_type()
        parts = self.current_command.split()
        if t == C_ARITHMETIC:
            return parts[0]
        if len(parts) >= 2:
            return parts[1]
        return None

    def arg2(self) -> Optional[int]:
        if self.current_command is None:
            return None
        parts = self.current_command.split()
        if len(parts) >= 3:
            return int(parts[2])
        return None

# CodeWriter -----------------------------------------------------------------
class CodeWriter:
    def __init__(self) -> None:
        self.asm_lines = []
        self._label_counter = itertools.count()
        self.current_vm_file = "Static"  # default prefix for static vars

    def set_file_name(self, filename: str) -> None:
        base = os.path.basename(filename)
        self.current_vm_file = os.path.splitext(base)[0]

    def _unique(self, base: str) -> str:
        return f"{base}${next(self._label_counter)}"

    def write_comment(self, comment: str) -> None:
        self.asm_lines.append(f"// {comment}")

    # Helper: push D onto stack
    def _push_d(self) -> None:
        self.asm_lines += ["@SP", "A=M", "M=D", "@SP", "M=M+1"]

    # Helper: pop stack into D
    def _pop_to_d(self) -> None:
        self.asm_lines += ["@SP", "AM=M-1", "D=M"]

    def write_arithmetic(self, command: str) -> None:
        self.write_comment(f"arithmetic {command}")
        if command == "add":
            self.asm_lines += [
                "@SP", "AM=M-1", "D=M",  # y
                "@SP", "AM=M-1", "M=M+D", "@SP", "M=M+1"
            ]
            return
        if command == "sub":
            self.asm_lines += [
                "@SP", "AM=M-1", "D=M",
                "@SP", "AM=M-1", "M=M-D", "@SP", "M=M+1"
            ]
            return
        if command == "and":
            self.asm_lines += [
                "@SP", "AM=M-1", "D=M",
                "@SP", "AM=M-1", "M=M&D", "@SP", "M=M+1"
            ]
            return
        if command == "or":
            self.asm_lines += [
                "@SP", "AM=M-1", "D=M",
                "@SP", "AM=M-1", "M=M|D", "@SP", "M=M+1"
            ]
            return
        if command == "neg":
            self.asm_lines += ["@SP", "A=M-1", "M=-M"]
            return
        if command == "not":
            self.asm_lines += ["@SP", "A=M-1", "M=!M"]
            return
        if command in ("eq", "gt", "lt"):
            label_true = self._unique(f"{command.upper()}_TRUE")
            label_end = self._unique(f"{command.upper()}_END")
            # x - y in D
            self.asm_lines += [
                "@SP", "AM=M-1", "D=M",       # D = y
                "@SP", "AM=M-1", "D=M-D"     # D = x - y
            ]
            jmp = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}[command]
            self.asm_lines += [
                f"@{label_true}", f"D;{jmp}",
                "@SP", "A=M", "M=0",
                f"@{label_end}", "0;JMP",
                f"({label_true})",
                "@SP", "A=M", "M=-1",
                f"({label_end})",
                "@SP", "M=M+1"
            ]
            return
        raise NotImplementedError(f"Unbekannter arithmetic Befehl: {command}")

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        self.write_comment(f"{command} {segment} {index}")
        if command == "push":
            if segment == "constant":
                self.asm_lines += [f"@{index}", "D=A"]
                self._push_d()
                return
            if segment == "local":
                self.asm_lines += ["@LCL", "D=M", f"@{index}", "A=D+A", "D=M"]
                self._push_d()
                return
            if segment == "argument":
                self.asm_lines += ["@ARG", "D=M", f"@{index}", "A=D+A", "D=M"]
                self._push_d()
                return
            if segment == "this":
                self.asm_lines += ["@THIS", "D=M", f"@{index}", "A=D+A", "D=M"]
                self._push_d()
                return
            if segment == "that":
                self.asm_lines += ["@THAT", "D=M", f"@{index}", "A=D+A", "D=M"]
                self._push_d()
                return
            if segment == "pointer":
                if index == 0:
                    self.asm_lines += ["@THIS", "D=M"]
                elif index == 1:
                    self.asm_lines += ["@THAT", "D=M"]
                else:
                    raise ValueError("pointer index must be 0 or 1")
                self._push_d()
                return
            if segment == "temp":
                addr = 5 + index
                self.asm_lines += [f"@R{addr}", "D=M"]
                self._push_d()
                return
            if segment == "static":
                symbol = f"{self.current_vm_file}.{index}"
                self.asm_lines += [f"@{symbol}", "D=M"]
                self._push_d()
                return
            raise NotImplementedError(f"Unbekanntes Segment (push): {segment}")

        if command == "pop":
            if segment in ("local", "argument", "this", "that"):
                base = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}[segment]
                # compute address -> R13
                self.asm_lines += [f"@{base}", "D=M", f"@{index}", "D=D+A", "@R13", "M=D"]
                # pop -> *R13
                self.asm_lines += ["@SP", "AM=M-1", "D=M", "@R13", "A=M", "M=D"]
                return
            if segment == "pointer":
                if index == 0:
                    dest = "THIS"
                elif index == 1:
                    dest = "THAT"
                else:
                    raise ValueError("pointer index must be 0 or 1")
                self.asm_lines += ["@SP", "AM=M-1", "D=M", f"@{dest}", "M=D"]
                return
            if segment == "temp":
                addr = 5 + index
                self.asm_lines += ["@SP", "AM=M-1", "D=M", f"@R{addr}", "M=D"]
                return
            if segment == "static":
                symbol = f"{self.current_vm_file}.{index}"
                self.asm_lines += ["@SP", "AM=M-1", "D=M", f"@{symbol}", "M=D"]
                return
            raise NotImplementedError(f"Unbekanntes Segment (pop): {segment}")

        raise NotImplementedError(f"Unbekannter Befehl: {command}")

    def write_to_file(self, vm_filename: str) -> None:
        asm_filename = vm_filename.replace(".vm", ".asm")
        if os.path.exists(asm_filename):
            if DEBUG:
                print(f"Overwriting {asm_filename}")
        with open(asm_filename, "w", encoding="utf-8") as f:
            for line in self.asm_lines:
                f.write(line + "\n")

# Driver --------------------------------------------------------------------
def translate_file(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        parser = VMParser(f)
        writer = CodeWriter()
        writer.set_file_name(path)
        while parser.has_more_commands():
            parser.advance()
            if parser.current_command is None:
                continue
            t = parser.command_type()
            if t == C_ARITHMETIC:
                cmd = parser.arg1()
                if cmd:
                    writer.write_arithmetic(cmd)
            elif t in (C_PUSH, C_POP):
                parts = parser.current_command.split()
                command, segment, index = parts[0], parts[1], int(parts[2])
                writer.write_push_pop(command, segment, index)
            else:
                # Projekt 7 benötigt sonst nichts
                writer.write_comment(f"unhandled: {parser.current_command}")
        writer.write_to_file(path)
        if DEBUG:
            print(f"Translated {path} -> {path.replace('.vm', '.asm')}")

def main() -> None:
    if len(sys.argv) < 2:
        path = input("Dateipfad (.vm oder Verzeichnis) angeben: ").strip()
    else:
        path = sys.argv[1]
    files = []
    if os.path.isdir(path):
        files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".vm")]
    else:
        files = [path]
    for vm in files:
        try:
            translate_file(vm)
            print(f"Translated: {vm}")
        except Exception as e:
            print(f"Fehler bei {vm}: {e}")

if __name__ == "__main__":
    main()
