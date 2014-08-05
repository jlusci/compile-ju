; ----------------------------------
; Hello World Program (calculating string length) - original from asmtutor.com
; modified for 64bit
; ----------------------------------



; ----------------------------------
; The .data section holds all the 'variables' your code will use
; Note that, other than the labels in the ".text" section, "msg" is the only user-defined word in this code.
SECTION .data
msg     db      'Hello World!', 0Ah     ; assign msg variable with your message string, followed by a newline character (0Ah)
; ----------------------------------



; ----------------------------------
; Sometimes there will be a .bss section, which (I think) reserves space on the stack for constants.
SECTION .bss
; ----------------------------------
; Not needed in this program



; ----------------------------------
; The .text section contains the main body of your code.
; Generally, it is followed by "global start".
; It tells the assembler that the "start" label is the subroutine that should be executed first on runtime.
; ----------------------------------
SECTION .text
global  start

; Subroutines are labelled just as below, with the name followed by a colon.
; In this instance, "start" has global scope, while ".nextchar" is a local label, and therefore can only be called while in "start".
; The period denotes the scope change.
; (Most of the following comments are straight from asmtutor.com . Always cite your sources!)
start:
 
    mov     rdi, msg        ; move the address of our message string into rdi
    mov     rax, rdi        ; move the address in rdi into rax as well (Both now point to the same segment in memory)
 
.nextchar:
    cmp     byte [rax], 0   ; compare the byte pointed to by rax at this address against zero (Zero is an end of string delimiter)
    jz      .finished       ; jump (if the zero flagged has been set) to the point in the code labeled '.finished'
    inc     rax             ; increment the address in rax by one byte (if the zero flagged has NOT been set)
    jmp     .nextchar       ; jump to the point in the code labeled '.nextchar'
 
.finished:
    sub     rax, rdi        ; subtract the address in rdi from the address in rax
                            ; remember both registers started pointing to the same address
                            ; but rax has been incremented one byte for each character in the message string
                            ; when you subtract one memory address from another of the same type
                            ; the result is number of segments between them - in this case the number of bytes
                            ; in other words, rax now equals the number of characters (in bytes) in our string

; Now we set up the "print to the screen" process
; Specific registers (4 of them) need to be set to make this work.
    mov     rdx, rax        ; rdx contains the length of the message
    mov     rsi, msg        ; rsi contains the message itself
    mov     rdi, 1          ; rdi defines the message destination (1 = STDOUT = the terminal for us)
    mov     rax, 0x2000004  ; rax defines what kind of syscall we will be doing (ending in 4 = SYS_WRITE)
    syscall                 ; now that the 4 registers are set correctly, poke the kernel to activate!
 
    mov     rdi, 0          ; these three lines exit the code. nothing else is printed, so we don't need to clean the stack.
    mov     rax, 0x2000001  ; ending in 1 = exit code!
    syscall                 ; poke the kernel.