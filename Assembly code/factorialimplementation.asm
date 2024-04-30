######################## Concreate Syntax ##############################

# Iterative factorial implementation 

# var x = 5  
# var ans = 1

# for x > 1 {
#   ans = ans * x
#   x = x - 1
# }
# fmt.Println(ans)

######################## Assembly code ##################################

.text
.globl main

main:   
    li      $t0, 6
    li      $t1, 1
    blez    $t0, end_loop # If $t0 is less than or equal to 0, jump to end_loop

factorial:
    mul     $t1, $t1, $t0
    addi    $t0, $t0, -1
    bgtz    $t0, factorial  #If $t0 is greater than 0, jump to factorial

end_loop: 
    move    $a0, $t1         # move the value in $t0 to $a0
    li      $v0, 1           # print integer system call
    syscall

# exit program
    li      $v0, 10     # exit program system call
    syscall


