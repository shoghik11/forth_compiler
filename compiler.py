import sys
import subprocess

RUNTIME = "runtime.s"

def forth_to_asm(tokens):
    asm = []
    asm.append('.globl _start\n_start:\n    call init')

    var_table = {}
    var_offset = 0

    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok == '+':
            asm.append('    call pop')
            asm.append('    movq %rax, %rbx')
            asm.append('    call pop')
            asm.append('    addq %rbx, %rax')
            asm.append('    call push')
        elif tok == '-':
            asm.append('    call pop')
            asm.append('    movq %rax, %rbx')
            asm.append('    call pop')
            asm.append('    subq %rbx, %rax')
            asm.append('    call push')
        elif tok == '*':
            asm.append('    call pop')
            asm.append('    movq %rax, %rbx')
            asm.append('    call pop')
            asm.append('    imulq %rbx, %rax')
            asm.append('    call push')
        elif tok == 'mod':
            asm.append('    call pop')
            asm.append('    movq %rax, %rbx')
            asm.append('    call pop')
            asm.append('    xorq %rdx, %rdx')
            asm.append('    idivq %rbx')
            asm.append('    movq %rdx, %rax')
            asm.append('    call push')
        elif tok == 'dup':
            asm.append('    call pop')
            asm.append('    movq %rax, %rbx')
            asm.append('    call push')
            asm.append('    movq %rbx, %rax')
            asm.append('    call push')
        elif tok == 'swap':
            asm.append('    call pop')
            asm.append('    movq %rax, %rbx')
            asm.append('    call pop')
            asm.append('    movq %rax, %rcx')
            asm.append('    movq %rbx, %rax')
            asm.append('    call push')
            asm.append('    movq %rcx, %rax')
            asm.append('    call push')
        elif tok == 'drop':
            asm.append('    call pop')  # ✅ Just remove top item
        elif tok == 'over':
            asm.append('    call pop')
            asm.append('    movq %rax, %rbx')
            asm.append('    call pop')
            asm.append('    movq %rax, %rcx')
            asm.append('    call push')
            asm.append('    movq %rbx, %rax')
            asm.append('    call push')
            asm.append('    movq %rcx, %rax')
            asm.append('    call push')
        elif tok == 'nip':
            asm.append('    call pop')            # pop top -> %rax
            asm.append('    movq %rax, %rbx')     # save top in %rbx
            asm.append('    call pop')            # pop second (discard)
            asm.append('    movq %rbx, %rax')     # restore top
            asm.append('    call push')           # push it back
        elif tok == 'tack' or tok == 'neg':
            asm.append('    call pop')
            asm.append('    negq %rax')
            asm.append('    call push')
        elif tok == '.':
            asm.append('    call pop')
            asm.append('    call print')
        elif tok == '.s':
            asm.append('    call dump_stack')
        elif tok == 'variable':
            name = tokens[i+1]
            var_table[name] = var_offset
            var_offset += 8
            i += 1
        elif tok in var_table:
            if i+1 < len(tokens) and tokens[i+1] == '!':
                asm.append('    call pop')
                asm.append(f'    movq %rax, var_{tok}(%rip)')
                i += 1
            elif i+1 < len(tokens) and tokens[i+1] == '@':
                asm.append(f'    movq var_{tok}(%rip), %rax')
                asm.append('    call push')
                i += 1
            else:
                raise Exception(f"Unexpected use of variable {tok}")
        elif tok.isdigit():
            asm.append(f'    movq ${tok}, %rax')
            asm.append('    call push')
        else:
            raise Exception(f"Unknown token: {tok}")
        i += 1

    asm.append('    movq $60, %rax')
    asm.append('    xorq %rdi, %rdi')
    asm.append('    syscall')

    if var_table:
        asm.append('\n.data')
        for name in var_table:
            asm.append('    .align 8')
            asm.append(f'var_{name}: .quad 0')

    return '\n'.join(asm)

def main():
    src = sys.argv[1]
    out_s = src.replace('.fs', '.s')
    out_o = src.replace('.fs', '.o')
    out_bin = src.replace('.fs', '')

    with open(src) as f:
        tokens = [t for t in f.read().split() if not t.startswith('\\')]

    asm = forth_to_asm(tokens)

    with open(out_s, 'w') as f:
        f.write(asm)

    subprocess.run(["as", "-o", out_o, RUNTIME, out_s], check=True)
    subprocess.run(["ld", "-o", out_bin, out_o], check=True)

if __name__ == "__main__":
    main()
