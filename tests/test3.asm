	b Lmain
L0:
	sw $ra, ($sp)
L1:
	lw $t1, -16($sp)
	sw $t1, -16($s0)
L2:
	lw $t1, -12($sp)
	sw $t1, -16($sp)
L3:
	addi $fp, $sp, 24
	lw $t0, -12($sp)
	sw $t0, -12($fp)
L4:
	addi $t0, $sp, -20
	sw $t0, -8($fp)
L5:
	lw $t0, -4($sp)
	sw $t0, -4($fp)
	addi $sp, $sp, 24
	jal L0
	addi $sp, $sp, -24
L6:
	lw $t1, -20($sp)
	sw $t1, -20($s0)
L7:
	lw $t1, -20($s0)
	lw $t0, -8($sp)
	sw $t1, ($t0)
	lw $ra, ($sp)
	jr $ra
L8:
	lw $ra, ($sp)
	jr $ra
L9:
	sw $ra, ($sp)
L10:
	addi $fp, $sp, 24
	lw $t0, -12($sp)
	sw $t0, -12($fp)
L11:
	addi $t0, $sp, -16
	sw $t0, -8($fp)
L12:
	lw $t0, -4($sp)
	sw $t0, -4($fp)
	addi $sp, $sp, 24
	jal L0
	addi $sp, $sp, -24
L13:
	lw $t1, -16($sp)
	sw $t1, -20($s0)
L14:
	lw $t1, -20($s0)
	lw $t0, -8($sp)
	sw $t1, ($t0)
	lw $ra, ($sp)
	jr $ra
L15:
	lw $ra, ($sp)
	jr $ra
L16:
	sw $ra, ($sp)
L17:
	lw $t1, -12($sp)
	lw $t0, -16($sp)
	sw $t1, ($t0)
L18:
	lw $ra, ($sp)
	jr $ra
L19:
	sw $ra, ($sp)
L20:
	li $t1, 1
	sw $t1, -12($sp)
L21:
	addi $fp, $sp, 24
	lw $t0, -16($sp)
	sw $t0, -12($fp)
L22:
	addi $t0, $sp, -12
	sw $t0, -16($fp)
L23:
	lw $t0, -4($sp)
	sw $t0, -4($fp)
	addi $sp, $sp, 24
	jal L16
	addi $sp, $sp, -24
L24:
	lw $ra, ($sp)
	jr $ra
Lmain:
L25:
	addi $sp, $sp, 24
	move $s0, $sp
L26:
	addi $fp, $sp, 24
	lw $t0, -12($s0)
	sw $t0, -12($fp)
L27:
	addi $t0, $sp, -16
	sw $t0, -16($fp)
L28:
	lw $t0, -4($sp)
	sw $t0, -4($fp)
	addi $sp, $sp, 24
	jal L16
	addi $sp, $sp, -24
L29:
	addi $fp, $sp, 20
	lw $t0, -20($s0)
	sw $t0, -12($fp)
L30:
	lw $t0, -4($sp)
	sw $t0, -4($fp)
	addi $sp, $sp, 20
	jal L19
	addi $sp, $sp, -20
L31:
	li $v0, 10 
	syscall