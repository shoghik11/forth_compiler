.data
stack_space:
    .zero 8000             # Reserve 8KB for the Forth stack
numbuf:
    .zero 32               # Buffer to store number string

.text
.global init
.global push
.global pop
.global print
.global dump_stack

# ----------------------------------------
# Stack pointer in %r12
# ----------------------------------------
init:
    lea stack_space+8000(%rip), %r12
    ret

# ----------------------------------------
# Push %rax onto the stack
# ----------------------------------------
push:
    subq $8, %r12
    movq %rax, (%r12)
    ret

# ----------------------------------------
# Pop value into %rax
# ----------------------------------------
pop:
    movq (%r12), %rax
    addq $8, %r12
    ret

# ----------------------------------------
# Print value in %rax with newline
# ----------------------------------------
print:
    # Setup buffer pointer
    lea numbuf+31(%rip), %rdi
    movb $0, (%rdi)          # null terminator
    movq %rdi, %rsi          # %rsi = string write ptr
    movq %rax, %rbx          # copy input value
    movq $10, %rcx           # divisor for base 10
    xorq %rdx, %rdx          # clear remainder
    movb $0, %r8b            # sign flag

    cmpq $0, %rbx
    jge .convert_loop

    negq %rbx
    movb $1, %r8b            # mark as negative

.convert_loop:
    xorq %rdx, %rdx
    movq %rbx, %rax
    divq %rcx
    addb $'0', %dl
    decq %rsi
    movb %dl, (%rsi)
    movq %rax, %rbx
    testq %rbx, %rbx
    jnz .convert_loop

    cmpb $0, %r8b
    je .append_newline

    decq %rsi
    movb $'-', (%rsi)

.append_newline:
    # Append newline after the number
    lea numbuf+31(%rip), %rdi
    movb $0x0a, (%rdi)

    # Print the number
    movq $1, %rax            # syscall: write
    movq $1, %rdi            # stdout
    movq %rsi, %rsi          # buffer pointer
    lea numbuf+32(%rip), %rdx
    subq %rsi, %rdx          # length = (end of buffer) - start
    syscall
    ret

# ----------------------------------------
# Dump entire stack (from bottom to top)
# ----------------------------------------
dump_stack:
    movq %r12, %r13                     # r13 = top of stack (low address)
    lea stack_space+8000(%rip), %r14   # r14 = bottom of stack (starting point)

.loop:
    cmpq %r14, %r13
    je .done                           # if we've reached bottom, we're done

    # Pop value from stack and print it
    movq (%r13), %rax                  # load value from stack into %rax
    call print                         # print value in %rax

    addq $8, %r13                      # move up the stack (increase r13)
    
    # Pop the value off the stack
    addq $8, %r12                       # remove value from stack

    jmp .loop

.done:
    ret



