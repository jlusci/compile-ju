; Fizzbuzz
; Compile with: nasm -f elf fizzbuzz.asm
; Link with (64 bit systems require elf_i386 option): ld -m elf_i386 fizzbuzz.o -o fizzbuzz
; Run with: ./fizzbuzz
 
%include        'functions.asm'
 
SECTION .data
fizz        db      'Fizz', 0h    ; a message string
buzz        db      'Buzz', 0h    ; a message string
 
SECTION .text
global  start
 
start:

    mov     r9, 0          ; initialise our checkFizz boolean variable
    mov     r10, 0         ; initialise our checkBuzz boolean variable
    mov     rsi, 0         ; initialise our counter variable
 
nextNumber:
    inc     rsi            ; increment our counter variable
 
.checkFizz:
    mov     rdx, 0         ; clear the rdx register - this will hold our remainder after division
    mov     rax, rsi       ; move the value of our counter into rax for division
    mov     rdi, 3         ; move our number to divide by into rdi (in this case the value is 3)
    div     rdi            ; divide rax by rdi
    mov     r10, rdx       ; move our remainder into r10 (our checkFizz boolean variable)
    cmp     r10, 0         ; compare if the remainder is zero (meaning the counter divides by 3)
    jne     .checkBuzz     ; if the remainder is not equal to zero jump to local label checkBuzz
    mov     rax, fizz      ; else move the address of our fizz string into rax for printing
    call    sprint         ; call our string printing function
 
.checkBuzz:
    mov     rdx, 0         ; clear the rdx register - this will hold our remainder after division
    mov     rax, rsi       ; move the value of our counter into rax for division
    mov     rdi, 5         ; move our number to divide by into rdi (in this case the value is 5)
    div     rdi            ; divide rax by rdi
    mov     r9, rdx        ; move our remainder into r10 (our checkBuzz boolean variable)
    cmp     r9, 0          ; compare if the remainder is zero (meaning the counter divides by 5)
    jne     .checkInt      ; if the remainder is not equal to zero jump to local label checkInt
    mov     rax, buzz      ; else move the address of our buzz string into rax for printing
    call    sprint         ; call our string printing function
 
.checkInt:
    cmp     r10, 0         ; r10 contains the remainder after the division in checkFizz
    je     .continue       ; if equal (counter divides by 3) skip printing the integer
    cmp     r9, 0          ; r9 contains the remainder after the division in checkBuzz
    je     .continue       ; if equal (counter divides by 5) skip printing the integer
    mov     rax, rsi       ; else move the value in rsi (our counter) into rax for printing
    call    iprint         ; call our integer printing function
 
.continue:
    mov     rax, 0Ah       ; move an ascii linefeed character into rax
    push    rax            ; push the address of rax onto the stack for printing
    mov     rax, rsp       ; get the stack pointer (address on the stack of our linefeed char)
    call    sprint         ; call our string printing function to print a line feed
    pop     rax            ; pop the stack so we don't waste resources
    cmp     rsi, 100       ; compare if our counter is equal to r11
    jne     nextNumber     ; if not equal jump to the start of the loop
 
    call    quit           ; else call our quit function