################ Concreate syntax ####################

# Write to the console integers:
# Println(17)

################ Assembly code #####################

.text
.global main 

main: 

    li $t0, 18
    addi $sp, $sp, -4
    sw $t0, 4($sp)
    addi $sp, $sp, 4
    sw $t0, 4($sp)
    addi $sp, $sp, 4
    sw $t0, 4($sp)
    li $t0, 17
    addi $sp, $sp, -4
    sw $t0, 4($sp)
    addi $sp, $sp, 4
    sw $t0, 4($sp)
    addi $sp, $sp, 4
    sw $t0, 4($sp)