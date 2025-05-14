# 🛠️ Forth-to-x86_64 Compiler

A simple compiler that translates a subset of the [Forth](https://en.wikipedia.org/wiki/Forth_(programming_language)) language into x86_64 assembly. The generated assembly is linked with a runtime library to produce native Linux binaries.

---

## 📦 Features

- Stack-based computation (using a manual stack in `.bss`)
- Arithmetic: `+ - * mod`
- Stack manipulation: `dup swap drop over nip`
- Output: `.` (print top of stack), `.s` (print full stack)
- Variables: `variable name`, `name @`, `value ! name`
- File-based compilation: reads `.fs`, produces `.s`, assembles to ELF binary
- Minimal runtime (`runtime.s`) with syscalls and stack setup

---

## 🚀 Getting Started

### 🔧 Requirements

- Python 3
- GNU `as` (assembler) and `ld` (linker) from `binutils`

### 📁 Project Structure
- **`compiler.py`**: Translates Forth source code into x86 Assembly.
- **`runtime.s`**: Provides a basic assembly runtime to support the compiled Forth code, including a data stack and basic input/output routines.
- **`test.fs`**: A sample Forth script used to test the compiler.



## 🛠️ How to Compile

```bash
# 1. Compile Forth source to assembly
python3 compiler.py test.fs

# 2. Run the program
./test
```

Assemble and link already done in python
```bash

as -o test.o runtime.s test.s
ld -o test test.o


