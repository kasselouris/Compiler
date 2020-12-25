	b Lmain
L0:
	sw $ra, ($sp)
L1:
	lw $t1, -12($sp)
	lw $t2, -12($sp)
	bgt $t1, $t2, L3
L2:
	b L5
L3:
	lw $t1, -12($sp)
	lw $t0, -8($sp)
	sw $t1, ($t0)
	lw $ra, ($sp)
	jr $ra
L4:
	b L6
L5:
	lw $t1, -16($sp)
	lw $t0, -8($sp)
	sw $t1, ($t0)
	lw $ra, ($sp)
	jr $ra
L6:
	lw $ra, ($sp)
	jr $ra
L7:
	sw $ra, ($sp)
L8:
	li $v0, 1
	lw $t2, -12($sp)
	move $a0, $t0
	syscall
L9:
	li $v0, 1
	lw $t2, -16($sp)
	move $a0, $t0
	syscall
L10:
	lw $t1, -12($sp)
	lw $t2, -12($sp)
	add $t1, $t1, $t2
	sw $t3, -24($sp)
L11:
	lw $t1, -24($sp)
	lw $t0, -20($sp)
	sw $t1, ($t0)
L12:
	lw $ra, ($sp)
	jr $ra
Lmain:
L13:
	addi $sp, $sp, 68
	move $s0, $sp
L14:
	li $t1, 1
	sw $t1, -12($s0)
L15:
	li $t1, 10
	sw $t1, -16($s0)
L16:
	li $t1, -1
	sw $t1, -32($s0)
L17:
	li $t1, 0
	sw $t1, -36($s0)
L18:
	addi $fp, $sp, 20
	lw $t0, -12($s0)
	sw $t0, -12($fp)
L19:
	lw $t0, -16($s0)
	sw $t0, -16($fp)
L20:
	addi $t0, $sp, -40
	sw $t0, -8($fp)
L21:
	lw $t0, -4($sp)
	sw $t0, -4($fp)
	addi $sp, $sp, 20
	jal L0
	addi $sp, $sp, -20
L22:
	addi $fp, $sp, 20
	lw $t0, -40($sp)
	sw $t0, -12($fp)
L23:
	lw $t0, -20($s0)
	sw $t0, -16($fp)
L24:
	addi $t0, $sp, -44
	sw $t0, -8($fp)
L25:
	lw $t0, -4($sp)
	sw $t0, -4($fp)
	addi $sp, $sp, 20
	jal L0
	addi $sp, $sp, -20
L26:
	lw $t1, -44($sp)
	sw $t1, -28($s0)
L27:
	lw $t1, -28($s0)
	sw $t1, -24($s0)
L28:
	addi $fp, $sp, 20
	lw $t0, -32($s0)
	sw $t0, -12($fp)
L29:
	lw $t0, -36($s0)
	sw $t0, -16($fp)
L30:
	addi $t0, $sp, -48
	sw $t0, -8($fp)
L31:
	lw $t0, -4($sp)
	sw $t0, -4($fp)
	addi $sp, $sp, 20
	jal L0
	addi $sp, $sp, -20
L32:
	lw $t1, -48($sp)
	sw $t1, -28($s0)
L33:
	lw $t1, -12($s0)
	lw $t2, -12($s0)
	beq $t1, $t2, L35
L34:
	b L37
L35:
	li $t1, 1
	sw $t1, -16($s0)
L36:
	b L51
L37:
	lw $t1, -12($s0)
	lw $t2, -12($s0)
	beq $t1, $t2, L39
L38:
	b L41
L39:
	lw $t1, -24($s0)
	sw $t1, -16($s0)
L40:
	b L51
L41:
	lw $t1, -12($s0)
	lw $t2, -12($s0)
	beq $t1, $t2, L43
L42:
	b L48
L43:
	lw $t1, -24($s0)
	lw $t2, -24($s0)
	add $t1, $t1, $t2
	sw $t3, -52($sp)
L44:
	lw $t1, -52($sp)
	lw $t2, -52($sp)
	add $t1, $t1, $t2
	sw $t3, -56($sp)
L45:
	lw $t1, -56($sp)
	lw $t2, -56($sp)
	div $t1, $t1, $t2
	sw $t3, -60($sp)
L46:
	lw $t1, -60($sp)
	sw $t1, -16($s0)
L47:
	b L51
L48:
	lw $t1, -24($s0)
	lw $t2, -24($s0)
	add $t1, $t1, $t2
	sw $t3, -64($sp)
L49:
	lw $t1, -64($sp)
	sw $t1, -16($s0)
L50:
	b L52
L51:
	b L33
L52:
	li $v0, 1
	lw $t2, -12($s0)
	move $a0, $t0
	syscall
L53:
	li $v0, 5
	syscall
	move $t0, $v0
	sw $t0, -20($s0)
L54:
	addi $fp, $sp, 28
	lw $t0, -20($s0)
	sw $t0, -12($fp)
L55:
	lw $t0, -16($s0)
	sw $t0, -16($fp)
L56:
	addi $t0, $sp, -12
	sw $t0, -20($fp)
L57:
	lw $t0, -4($sp)
	sw $t0, -4($fp)
	addi $sp, $sp, 28
	jal L7
	addi $sp, $sp, -28
L58:
	li $v0, 10 
	syscall