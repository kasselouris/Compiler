	b Lmain
L0:
	sw $ra, ($sp)
L1:
	lw $t1, -16($sp)
	lw $t2, -16($sp)
	add $t1, $t1, $t2
	sw $t3, -20($sp)
L2:
	lw $t1, -20($sp)
	sw $t1, -16($sp)
L3:
	lw $ra, ($sp)
	jr $ra
L4:
	sw $ra, ($sp)
L5:
	lw $t0, -12($sp)
	lw $t1, ($t0)
	lw $t0, -12($sp)
	lw $t2, ($t0)
	add $t1, $t1, $t2
	sw $t3, -24($sp)
L6:
	lw $t1, -24($sp)
	lw $t2, -24($sp)
	add $t1, $t1, $t2
	sw $t3, -28($sp)
L7:
	lw $t1, -28($sp)
	sw $t1, -20($sp)
L8:
	lw $ra, ($sp)
	jr $ra
L9:
	sw $ra, ($sp)
L10:
	lw $t1, -20($sp)
	lw $t2, -20($sp)
	add $t1, $t1, $t2
	sw $t3, -24($sp)
L11:
	lw $t1, -24($sp)
	sw $t1, -20($sp)
L12:
	lw $ra, ($sp)
	jr $ra
L13:
	sw $ra, ($sp)
L14:
	lw $t1, -12($sp)
	lw $t2, -12($sp)
	add $t1, $t1, $t2
	sw $t3, -24($sp)
L15:
	lw $t1, -24($sp)
	lw $t2, -24($sp)
	div $t1, $t1, $t2
	sw $t3, -28($sp)
L16:
	lw $t1, -28($sp)
	sw $t1, -16($sp)
L17:
	lw $ra, ($sp)
	jr $ra
L18:
	sw $ra, ($sp)
L19:
	lw $ra, ($sp)
	jr $ra
L20:
	sw $ra, ($sp)
L21:
	lw $t1, -12($sp)
	lw $t2, -12($sp)
	add $t1, $t1, $t2
	sw $t3, -24($sp)
L22:
	lw $t1, -24($sp)
	sw $t1, -20($sp)
L23:
	lw $ra, ($sp)
	jr $ra
Lmain:
L24:
	addi $sp, $sp, 32
	move $s0, $sp
L25:
	lw $t1, -16($s0)
	lw $t2, -16($s0)
	add $t1, $t1, $t2
	sw $t3, -24($sp)
L26:
	lw $t1, -24($sp)
	lw $t2, -24($sp)
	add $t1, $t1, $t2
	sw $t3, -28($sp)
L27:
	lw $t1, -28($sp)
	sw $t1, -12($s0)
L28:
	li $v0, 10 
	syscall