################ Concreate syntax ####################

# Write to the console integers:
# Println(17)

################ Assembly code #####################

.text
.global main 

main: 
    li $a0, 17  # load the immediate value 17 into $a0, the argument for syscall
    li $v0, 1   # load the immediate value 1 into $v0, the syscall for print integer
    syscall     # execute the print syscall
    
    # Print a newline character
    li $a0, 0x0A     # Load newline character '\n' (ASCII 10) into $a0
    li $v0, 11       # Load 11 into $v0, the system call for printing a character
    syscall          # Execute the print syscall

    # Exit the program
    li $v0, 10       # Load 10 into $v0, the system call for exiting a program
    syscall          # Execute the exit syscall