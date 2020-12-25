	b Lmain
Lmain:
L0:
	addi $sp, $sp, 48
	move $s0, $sp
L1:
	li $t1, 1
	sw $t1, -12($s0)
L2:
	li $t1, 1000
	li $t2, 1000
	sub $t1, $t1, $t2
	sw $t3, -28($sp)
L3:
	lw $t1, -28($sp)
	lw $t2, -28($sp)
	mul $t1, $t1, $t2
	sw $t3, -32($sp)
L4:
	lw $t1, -32($sp)
	lw $t2, -32($sp)
	div $t1, $t1, $t2
	sw $t3, -36($sp)
L5:
	lw $t1, -36($sp)
	sw $t1, -24($s0)
L6:
	lw $t1, -12($s0)
	lw $t2, -12($s0)
	add $t1, $t1, $t2
	sw $t3, -40($sp)
L7:
	lw $t1, -40($sp)
	sw $t1, -16($s0)
L8:
	lw $t1, -12($s0)
	lw $t2, -12($s0)
	add $t1, $t1, $t2
	sw $t3, -44($sp)
L9:
	lw $t1, -44($sp)
	lw $t2, -44($sp)
	ble $t1, $t2, L11
L10:
	b L15
L11:
	lw $t1, -16($s0)
	lw $t2, -16($s0)
	blt $t1, $t2, L13
L12:
	b L15
L13:
	lw $t1, -12($s0)
	lw $t2, -12($s0)
	bgt $t1, $t2, L15
L14:
	b L35
L15:
	lw $t1, -24($s0)
	lw $t2, -24($s0)
	beq $t1, $t2, L17
L16:
	b L19
L17:
	li $t1, 2
	sw $t1, -20($s0)
L18:
	b L19
L19:
	lw $t1, -24($s0)
	lw $t2, -24($s0)
	beq $t1, $t2, L21
L20:
	b L23
L21:
	li $t1, 4
	sw $t1, -20($s0)
L22:
	b L24
L23:
	li $t1, 0
	sw $t1, -20($s0)
L24:
	lw $t1, -12($s0)
	lw $t2, -12($s0)
	blt $t1, $t2, L26
L25:
	b L34
L26:
	lw $t1, -12($s0)
	lw $t2, -12($s0)
	beq $t1, $t2, L28
L27:
	b L33
L28:
	lw $t1, -16($s0)
	lw $t2, -16($s0)
	beq $t1, $t2, L30
L29:
	b L32
L30:
	li $t1, 2
	sw $t1, -20($s0)
L31:
	b L28
L32:
	b L33
L33:
	b L24
L34:
	b L8
L35:
	li $v0, 10 
	syscall