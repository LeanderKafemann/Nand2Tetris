"""
VM -> Hack ASM Translator (Projekt 8)
Unterstützt: arithmetic, push/pop, label, goto, if-goto, function, call, return
Bei Verzeichnis-Input: erzeugt eine einzige .asm Datei und fügt Bootstrap (SP=256; call Sys.init) hinzu.
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
C_LABEL = "C_LABEL"
C_GOTO = "C_GOTO"
C_IF = "C_IF"
C_FUNCTION = "C_FUNCTION"
C_RETURN = "C_RETURN"
C_CALL = "C_CALL"

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
        if cmd == "label":
            return C_LABEL
        if cmd == "goto":
            return C_GOTO
        if cmd == "if-goto":
            return C_IF
        if cmd == "function":
            return C_FUNCTION
        if cmd == "call":
            return C_CALL
        if cmd == "return":
            return C_RETURN
        return C_ARITHMETIC

    def arg1(self) -> Optional[str]:
        if self.current_command is None:
            return None
        t = self.command_type()
        parts = self.current_command.split()
        if t == C_RETURN:
            return None
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
        self.current_function = ""       # for function-scoped labels

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

    def _full_label(self, label: str) -> str:
        if self.current_function:
            return f"{self.current_function}${label}"
        return label

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

    # Flow commands
    def write_label(self, label: str) -> None:
        full = self._full_label(label)
        self.write_comment(f"label {label}")
        self.asm_lines.append(f"({full})")

    def write_goto(self, label: str) -> None:
        full = self._full_label(label)
        self.write_comment(f"goto {label}")
        self.asm_lines += [f"@{full}", "0;JMP"]

    def write_if(self, label: str) -> None:
        full = self._full_label(label)
        self.write_comment(f"if-goto {label}")
        self._pop_to_d()
        self.asm_lines += [f"@{full}", "D;JNE"]

    # Function/Call/Return
    def write_function(self, name: str, n_vars: int) -> None:
        self.write_comment(f"function {name} {n_vars}")
        # set current function context (used for labels inside function)
        self.current_function = name
        # function entry label
        self.asm_lines.append(f"({name})")
        # initialize n local vars to 0
        for _ in range(n_vars):
            self.asm_lines += ["@0", "D=A"]
            self._push_d()

    def write_call(self, name: str, n_args: int) -> None:
        self.write_comment(f"call {name} {n_args}")
        return_label = self._unique(f"RET_{name}")
        # push return address
        self.asm_lines += [f"@{return_label}", "D=A"]
        self._push_d()
        # push LCL, ARG, THIS, THAT
        for reg in ("LCL", "ARG", "THIS", "THAT"):
            self.asm_lines += [f"@{reg}", "D=M"]
            self._push_d()
        # ARG = SP - n_args - 5
        self.asm_lines += ["@SP", "D=M", f"@{n_args + 5}", "D=D-A", "@ARG", "M=D"]
        # LCL = SP
        self.asm_lines += ["@SP", "D=M", "@LCL", "M=D"]
        # goto function
        self.asm_lines += [f"@{name}", "0;JMP"]
        # return label
        self.asm_lines.append(f"({return_label})")

    def write_return(self) -> None:
        self.write_comment("return")
        # FRAME = LCL -> R13
        self.asm_lines += ["@LCL", "D=M", "@R13", "M=D"]
        # RET = *(FRAME - 5) -> R14
        self.asm_lines += ["@R13", "D=M", "@5", "A=D-A", "D=M", "@R14", "M=D"]
        # *ARG = pop()
        self.asm_lines += ["@SP", "AM=M-1", "D=M", "@ARG", "A=M", "M=D"]
        # SP = ARG + 1
        self.asm_lines += ["@ARG", "D=M", "@SP", "M=D", "@SP", "M=M+1"]
        # THAT = *(FRAME-1)
        self.asm_lines += ["@R13", "AM=M-1", "D=M", "@THAT", "M=D"]
        # THIS = *(FRAME-2)
        self.asm_lines += ["@R13", "AM=M-1", "D=M", "@THIS", "M=D"]
        # ARG = *(FRAME-3)
        self.asm_lines += ["@R13", "AM=M-1", "D=M", "@ARG", "M=D"]
        # LCL = *(FRAME-4)
        self.asm_lines += ["@R13", "AM=M-1", "D=M", "@LCL", "M=D"]
        # goto RET
        self.asm_lines += ["@R14", "A=M", "0;JMP"]

    def write_init(self) -> None:
        self.write_comment("bootstrap")
        # SP = 256
        self.asm_lines += ["@256", "D=A", "@SP", "M=D"]
        # call Sys.init
        self.write_call("Sys.init", 0)

    def write_to_file(self, asm_filename: str) -> None:
        if os.path.exists(asm_filename):
            if DEBUG:
                print(f"Overwriting {asm_filename}")
        with open(asm_filename, "w", encoding="utf-8") as f:
            for line in self.asm_lines:
                f.write(line + "\n")

# Driver --------------------------------------------------------------------
def translate_files(files: list[str], output_asm: Optional[str] = None) -> None:
    writer = CodeWriter()
    # If multiple files target -> write bootstrap
    if output_asm is not None and len(files) > 1:
        writer.write_init()
    elif output_asm is not None and any(True for _ in files):  # if directory mode we still want bootstrap
        # In directory mode files>1 covered above. Keeping this line if desired to always bootstrap when output provided.
        pass

    for vm in files:
        writer.set_file_name(vm)
        with open(vm, "r", encoding="utf-8") as f:
            parser = VMParser(f)
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
                elif t == C_LABEL:
                    lbl = parser.arg1()
                    if lbl:
                        writer.write_label(lbl)
                elif t == C_GOTO:
                    lbl = parser.arg1()
                    if lbl:
                        writer.write_goto(lbl)
                elif t == C_IF:
                    lbl = parser.arg1()
                    if lbl:
                        writer.write_if(lbl)
                elif t == C_FUNCTION:
                    name = parser.arg1() or ""
                    n = parser.arg2() or 0
                    writer.write_function(name, n)
                elif t == C_CALL:
                    name = parser.arg1() or ""
                    n = parser.arg2() or 0
                    writer.write_call(name, n)
                elif t == C_RETURN:
                    writer.write_return()
                else:
                    writer.write_comment(f"unhandled: {parser.current_command}")

    # write output
    if output_asm is None and len(files) == 1:
        out = files[0].replace(".vm", ".asm")
    else:
        out = output_asm
    if out is None:
        raise RuntimeError("No output filename specified")
    writer.write_to_file(out)
    if DEBUG:
        print(f"Translated {len(files)} files -> {out}")

def main() -> None:
    if len(sys.argv) < 2:
        path = input("Dateipfad (.vm oder Verzeichnis) angeben: ").strip()
    else:
        path = sys.argv[1]
    files = []
    output_asm = None
    if os.path.isdir(path):
        vm_files = sorted([os.path.join(path, f) for f in os.listdir(path) if f.endswith(".vm")])
        files = vm_files
        base = os.path.basename(os.path.normpath(path))
        output_asm = os.path.join(path, base + ".asm")
    else:
        files = [path]
        output_asm = None

    try:
        translate_files(files, output_asm)
        print(f"Translated: {len(files)} file(s)")
    except Exception as e:
        print(f"Fehler: {e}")
    input("Press Enter to continue...")

if __name__ == "__main__":
    main()