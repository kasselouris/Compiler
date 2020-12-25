	b Lmain
L0:
	sw $ra, ($sp)
L1:
	lw $t1, -16($s0)
	sw $t1, -20($s0)
L2:
	lw $t1, -12($sp)
	lw $t0, -4($sp)
	addi $t0, $t0, -16
	lw $t0, ($t0)
	sw $t1, ($t0)
L3:
	lw $ra, ($sp)
	jr $ra
L4:
	sw $ra, ($sp)
L5:
	li $t1, 2
	sw $t1, -16($s0)
L6:
	addi $fp, $sp, 16
	lw $t0, -12($sp)
	sw $t0, -12($fp)
L7:
	addi $t0, $sp, -20
	sw $t0, -8($fp)
L8:
	sw $sp, -4($fp)
	addi $sp, $sp, 16
	jal L0
	addi $sp, $sp, -16
L9:
	addi $fp, $sp, 16
	lw $t0, -20($sp)
	sw $t0, -12($fp)
L10:
	addi $t0, $sp, -24
	sw $t0, -8($fp)
L11:
	sw $sp, -4($fp)
	addi $sp, $sp, 16
	jal L0
	addi $sp, $sp, -16
L12:
	lw $t1, -24($sp)
	sw $t1, -12($sp)
L13:
	li $v0, 1
	lw $t2, -12($sp)
	move $a0, $t0
	syscall
L14:
	lw $ra, ($sp)
	jr $ra
Lmain:
L15:
	addi $sp, $sp, 28
	move $s0, $sp
L16:
	li $t1, 3
	sw $t1, -12($s0)
L17:
	li $t1, 4
	sw $t1, -16($s0)
L18:
	addi $fp, $sp, 28
	lw $t0, -12($s0)
	sw $t0, -12($fp)
L19:
	addi $t0, $sp, -16
	sw $t0, -16($fp)
L20:
	lw $t0, -4($sp)
	sw $t0, -4($fp)
	addi $sp, $sp, 28
	jal L4
	addi $sp, $sp, -28
L21:
	li $v0, 1
	lw $t2, -16($s0)
	move $a0, $t0
	syscall
L22:
	lw $t1, -20($s0)
	lw $t2, -20($s0)
	add $t1, $t1, $t2
	sw $t3, -24($sp)
L23:
	lw $t1, -12($s0)
	lw $t2, -12($s0)
	bne $t1, $t2, L25
L24:
	b L27
L25:
	li $v0, 1
	lw $t2, -20($s0)
	move $a0, $t0
	syscall
L26:
	b L27
L27:
	li $v0, 10 
	syscall