#Apostolos Kasselouris, A.M:2994, username:cse52994
#Python version 3.6.9

import string
import sys

################
#Lexical states#
################
#state0 - whitespace/begin
#state1 - identifier(id)
#state2 - constant
#state3 - <
#state4 - >
#state5 - :
#state6 - comments(/)
#state7 - line comments(//)
#state8 - variable length comments(/* */)

#########################
#define global variables#
#########################
#lexical/syntax variables
token = '' #string returned by lex
tokenID = '' #id returned by lex
state = 0 #initialize state
line_num = 1 #initialize line of file
buffer = [] #temporarily storage of tokens
counter = 0 #useful for counting id size(max size = 30)
lookAhead_flag = False #true if we secretly looked one byte ahead
c = '' #contains the secretly looked byte
###
error = -1 #ended due to an error
OK = -2 #ended correctly
#intermediate variables(quads)
quadList = {}	#dictionary
nextLabel = 0
temp_value = 0
program_name = ''
#symbol table variables
scopeList = []
programFramelength = 0
#final code variables
programStartQuad = 0	#will remain 0 if we have no functions/procedures
parSerialNum = 0


############################################################
#List of things used in LEXICAL ANALYZER based on Minimal++#
############################################################
letters = list(string.ascii_letters)
numbers = list(string.digits)
specialChar = ['+','-','*','/',
	'<','>','=',
	';',',',':',
	'(',')','[',']','{','}']
whitespaces = list(string.whitespace)
bindedWords = ['program','declare','if','else','while','doublewhile',
	'loop','exit','forcase','incase','when','default','not','and','or',
	'function','procedure','call','return','in','inout','input','print', 'then']





############################
#SYMBOL TABLE CODE(CLASSES)#
############################
#Entities
class Entity:
	def __init__(self, name, entityType):
		self.name = name
		self.entityType = entityType

	def printEntity(self):
		return "name: "+self.name+", type: "+self.entityType

class Variable(Entity):
	def __init__(self, name, entityType, offset):
		super().__init__(name, entityType)
		self.offset = offset

	def printEntity(self):
		return super().printEntity()+", offset: "+str(self.offset)

class FunctionOrProcedure(Entity):
	def __init__(self, name, entityType):
		super().__init__(name, entityType)
		self.startQuad = 0
		self.argumentList = []
		self.framelength = 12

	def printEntity(self):
		fp = super().printEntity() + ", StartQuad: " + str(self.startQuad) + ", "
		for i in self.argumentList:
			fp = fp + i.printArgument() + ", "
		fp = fp + "Framelength: " + str(self.framelength)
		return fp

class Constant(Entity):	#no need on minimal++
	def __init__(self, name, entityType, constantValue):
		super().__init__(name, entityType)
		self.constantValue = constantValue

	def printEntity(self):
		return super().printEntity()+", constantValue: "+str(self.constantValue)

class Parameter(Entity):
	def __init__(self, name, entityType, parMode, offset):
		super().__init__(name, entityType)
		self.parMode = parMode
		self.offset = offset

	def printEntity(self):
		return super().printEntity()+", parMode: "+self.parMode+", offset: "+str(self.offset)

class TempVariable(Entity):
	def __init__(self, name, entityType, offset):
		super().__init__(name, entityType)
		self.offset = offset

	def printEntity(self):
		return super().printEntity()+", offset: "+str(self.offset)

#scope
class Scope:
	def __init__(self, nestingLevel):
		self.nestingLevel = nestingLevel
		self.entityList = []
		self.framelength = 12	

	def printScope(self):
		sc = "NestingLevel: " + str(self.nestingLevel) + "\n"
		for i in self.entityList:
			sc = sc + i.printEntity() + "\n"
		sc = sc + "Framelength: " + str(self.framelength)
		return sc

#Argument
class Argument:
	def __init__(self, mode):
		self.mode = mode

	def printArgument(self):
		return "(Mode: "+ self.mode +")"

#defs
def addScope(nestingLevel):
	s = Scope(nestingLevel)
	if(len(scopeList) == 0):
		s.nestingLevel = 0
	else:
		s.nestingLevel = scopeList[-1].nestingLevel+1
	scopeList.append(s)

def deleteScope():
	del scopeList[-1]

def addVariable(name, entityType, offset, entityList):
	var = Variable(name, entityType, offset)
	entityList.append(var)

def addTempVariable(name, entityType, offset, entityList):
	tempVar = TempVariable(name, entityType, offset)
	entityList.append(tempVar)

def addFunction(name, entityType, entityList):
	func = FunctionOrProcedure(name, entityType)
	entityList.append(func)

def addProcedure(name, entityType, entityList):
	proc = FunctionOrProcedure(name, entityType)
	entityList.append(proc)

def addParameter(name, entityType, parMode, offset, entityList):
	par = Parameter(name, entityType, parMode, offset)
	entityList.append(par)

def addArgument(aMode, argumentList):
	arg = Argument(aMode)
	argumentList.append(arg)
	return arg

def searchEntity(name):
	if(name == program_name):	#for program entity
		return None, 0
	for i in range(len(scopeList)-1, -1, -1):	#range(start, stop, step)
		for entity in scopeList[i].entityList:
			if(entity.name == name):
				return entity, scopeList[i].nestingLevel
	print("Error: Entity '"+ name +"' not found, line "+str(line_num)+"!")
	sys.exit(1)

def printScopeList():	#used for testing
	print("SYMBOL TABLE:\n##################")
	for i in scopeList:
		print(i.printScope()+"\n")





###################
#INTERMEDIATE CODE#
###################
def nextquad():
	return str(nextLabel)

def genquad(op=None, x='_', y='_', z='_'):
	global nextLabel
	quadList[nextLabel] = [op, x , y, z]
	nextLabel+=1

def newtemp():
	global temp_value
	temp = 'T_'+str(temp_value)
	offset = scopeList[-1].framelength
	addTempVariable(temp, "TempVariable", offset, scopeList[-1].entityList)
	scopeList[-1].framelength = scopeList[-1].entityList[-1].offset+4
	temp_value+=1
	return temp

def emptylist():
	return []

def makelist(x):
	newList = []
	newList.append(x)
	return newList

def merge(list1, list2):
	return (list1+list2)

def backpatch(qlist, z):
	global quadList
	for label in quadList:
		if str(label) in qlist:
			quadList[label][3] = z

#int file that contains all quads
def create_int_file():
	for quad in quadList:
		intFile.write(str(quad)+": " + str(quadList[quad]) + '\n')
	intFile.close()

#transform minimal++ to c
def create_c_file():
	global program_name
	flag = False 	#skip all minimal++ functions and procedures and go to main
	cFile.write("#include <stdio.h>\n\n")
	for i in quadList:
		#main() and variables declaration
		if(quadList[i][0] == "begin_block" and quadList[i][1] == program_name):
			flag = True 	#from now on we will write to .c
			cFile.write("int main(){\n")
			cFile.write("\tint ")
			#declares
			for i in scopeList[0].entityList:
				if(i.entityType == "Variable" or i.entityType == "TempVariable"):
					cFile.write(i.name + ", ")
			cFile.seek(cFile.tell()-2)
			cFile.write(";\n")
		#assign
		elif(quadList[i][0] == ":=" and flag == True):
			cFile.write("\tL_"+str(i)+": "+ str(quadList[i][3]) +" = "+ str(quadList[i][1]) +";	//"+ str(quadList[i]) +"\n")
		#operators
		elif(quadList[i][0] == "+" and flag == True):
			cFile.write("\tL_"+str(i)+": "+ str(quadList[i][3]) +" = "+ str(quadList[i][1]) +" + "+ str(quadList[i][2]) +";	//"+ str(quadList[i]) +"\n")
		elif(quadList[i][0] == "-" and flag == True):
			cFile.write("\tL_"+str(i)+": "+ str(quadList[i][3]) +" = "+ str(quadList[i][1]) +" - "+ str(quadList[i][2]) +";	//"+ str(quadList[i]) +"\n")
		elif(quadList[i][0] == "*" and flag == True):
			cFile.write("\tL_"+str(i)+": "+ str(quadList[i][3]) +" = "+ str(quadList[i][1]) +" * "+ str(quadList[i][2]) +";	//"+ str(quadList[i]) +"\n")
		elif(quadList[i][0] == "/" and flag == True):
			cFile.write("\tL_"+str(i)+": "+ str(quadList[i][3]) +" = "+ str(quadList[i][1]) +" / "+ str(quadList[i][2]) +";	//"+ str(quadList[i]) +"\n")
		#comparisons
		elif(quadList[i][0] == "<" and flag == True):
			cFile.write("\tL_"+str(i)+": if("+ str(quadList[i][1]) +" < "+ str(quadList[i][2]) +") goto L_"+ str(quadList[i][3]) +";	//"+ str(quadList[i]) +"\n")
		elif(quadList[i][0] == ">" and flag == True):
			cFile.write("\tL_"+str(i)+": if("+ str(quadList[i][1]) +" > "+ str(quadList[i][2]) +") goto L_"+ str(quadList[i][3]) +";	//"+ str(quadList[i]) +"\n")
		elif(quadList[i][0] == "<=" and flag == True):
			cFile.write("\tL_"+str(i)+": if("+ str(quadList[i][1]) +" <= "+ str(quadList[i][2]) +") goto L_"+ str(quadList[i][3]) +";	//"+ str(quadList[i]) +"\n")
		elif(quadList[i][0] == ">=" and flag == True):
			cFile.write("\tL_"+str(i)+": if("+ str(quadList[i][1]) +" >= "+ str(quadList[i][2]) +") goto L_"+ str(quadList[i][3]) +";	//"+ str(quadList[i]) +"\n")
		elif(quadList[i][0] == "=" and flag == True):
			cFile.write("\tL_"+str(i)+": if("+ str(quadList[i][1]) +" = "+ str(quadList[i][2]) +") goto L_"+ str(quadList[i][3]) +";	//"+ str(quadList[i]) +"\n")
		elif(quadList[i][0] == "<>" and flag == True):
			cFile.write("\tL_"+str(i)+": if("+ str(quadList[i][1]) +" != "+ str(quadList[i][2]) +") goto L_"+ str(quadList[i][3]) +";	//"+ str(quadList[i]) +"\n")
		#input
		elif(quadList[i][0] == "inp" and flag == True):
			cFile.write("\tL_"+str(i)+": "+ 'scanf("%d", &'+str(quadList[i][1]) +");	//"+ str(quadList[i]) +"\n")
		#output
		elif(quadList[i][0] == "out" and flag == True):	
			cFile.write("\tL_"+str(i)+": "+ 'printf("%d\\n", '+str(quadList[i][1]) +");	//"+ str(quadList[i]) +"\n")
		#return 
		elif(quadList[i][0] ==  "retv" and flag == True):
			cFile.write("\tL_"+str(i)+": return " + str(quadList[i][1]) +";	//"+ str(quadList[i]) +"\n")
		#jump
		elif(quadList[i][0] == "jump" and flag == True):
			cFile.write("\tL_"+str(i)+":"+ " goto L_"+str(quadList[i][3]) +";	//"+ str(quadList[i]) +"\n")
		#halt
		elif(quadList[i][0] == "halt" and flag == True):
			cFile.write("\tL_"+str(i)+ ": return 0;	//"+ str(quadList[i]) +"\n")
			cFile.write("}")





######################
#FINAL CODE(ASSEMBLY)#
######################
def gnvlcode(v):
	entity, nstLvl = searchEntity(v)
	current_level = scopeList[-1].nestingLevel
	asmFile.write("	lw $t0, -4($sp)\n")
	for i in range(current_level, nstLvl+1, -1):
		asmFile.write("	lw $t0, -4($t0)\n")
	asmFile.write("	addi $t0, $t0, -"+ str(entity.offset) +"\n")
	
def loadvr(v,r):
	if(v.isdigit()):					#unsinged integers
		asmFile.write("	li $t"+str(r)+", "+str(v)+"\n")
	elif(v[0] == '+' or v[0] == '-'):	#signed integers
		temp = v[1:]
		if(temp.isdigit()):
			asmFile.write("	li $t"+str(r)+", "+str(v)+"\n")
		else:
			print("Error loading an unsigned number to a register in line "+str(line_num)+"!")
			sys.exit(-1)
	else:
		current_level = scopeList[-1].nestingLevel
		entity, nstLvl = searchEntity(v)
		if(nstLvl == 0 and entity.entityType == "Variable"):	#v global variable in main
			asmFile.write("	lw $t"+str(r)+", -"+str(entity.offset)+"($s0)\n")
		elif(nstLvl == current_level and (entity.entityType == "Variable" or 
				(entity.entityType == "Parameter" and entity.parMode == "in") or entity.entityType == "TempVariable" )):	#v local variable or parameter passed by value or temp variable
			asmFile.write("	lw $t"+str(r)+", -"+str(entity.offset)+"($sp)\n")
		elif(nstLvl == current_level and entity.entityType == "Parameter" and entity.parMode == "inout"):	#parameter passed by reference
			asmFile.write("	lw $t0, -"+str(entity.offset)+"($sp)\n")
			asmFile.write("	lw $t"+str(r)+", ($t0)\n")
		elif(nstLvl < current_level and (entity.entityType == "Variable" or (entity.entityType == "Parameter" and entity.parMode == "in"))):	#local variable or parameter passed by value on a lower nesting level
			gnvlcode(v)
			asmFile.write("	lw $t"+str(r)+", ($t0)\n")
		elif(nstLvl < current_level and entity.entityType == "Parameter" and entity.parMode == "inout"):	#parameter passed by reference on a lower nesting level
			gnvlcode(v)
			asmFile.write("	lw $t0, ($t0)\n")
			asmFile.write("	lw $t"+str(r)+", ($t0)\n")
		else:
			print("Error loading a value to a register in line "+str(line_num)+"!")
			sys.exit(-1)

def storerv(r,v):
	current_level = scopeList[-1].nestingLevel
	entity, nstLvl = searchEntity(v)
	if(nstLvl == 0 and entity.entityType == "Variable"):	#v global variable in main
		asmFile.write("	sw $t"+str(r)+", -"+str(entity.offset)+"($s0)\n")
	elif(nstLvl == current_level and (entity.entityType == "Variable" or 
			(entity.entityType == "Parameter" and entity.parMode == "in") or entity.entityType == "TempVariable" )):	#v local variable or parameter passed by value or temp variable
		asmFile.write("	sw $t"+str(r)+", -"+str(entity.offset)+"($sp)\n")
	elif(nstLvl == current_level and entity.entityType == "Parameter" and entity.parMode == "inout"):	#parameter passed by reference
		asmFile.write("	lw $t0, -"+str(entity.offset)+"($sp)\n")
		asmFile.write("	sw $t"+str(r)+", ($t0)\n")
	elif(nstLvl < current_level and (entity.entityType == "Variable" or (entity.entityType == "Parameter" and entity.parMode == "in"))):	#local variable or parameter passed by value on a lower nesting level
		gnvlcode(v)
		asmFile.write("	sw $t"+str(r)+", ($t0)\n")
	elif(nstLvl < current_level and entity.entityType == "Parameter" and entity.parMode == "inout"):	#parameter passed by reference on a lower nesting level
		gnvlcode(v)
		asmFile.write("	lw $t0, ($t0)\n")
		asmFile.write("	sw $t"+str(r)+", ($t0)\n")
	else:
		print("Error storing a value in line "+str(line_num)+"!")
		sys.exit(-1)

def create_assembly_file(quad, name):	#main final code function
	global parSerialNum
	#comparisons
	if(quadList[quad][0] == "="):
		asmFile.write("L"+str(quad)+":\n")
		loadvr(quadList[quad][1], 1)
		loadvr(quadList[quad][1], 2)
		asmFile.write("	beq $t1, $t2, L"+quadList[quad][3]+"\n")
	elif(quadList[quad][0] == "<>"):
		asmFile.write("L"+str(quad)+":\n")
		loadvr(quadList[quad][1], 1)
		loadvr(quadList[quad][1], 2)
		asmFile.write("	bne $t1, $t2, L"+quadList[quad][3]+"\n")
	elif(quadList[quad][0] == ">"):
		asmFile.write("L"+str(quad)+":\n")
		loadvr(quadList[quad][1], 1)
		loadvr(quadList[quad][1], 2)
		asmFile.write("	bgt $t1, $t2, L"+quadList[quad][3]+"\n")
	elif(quadList[quad][0] == "<"):
		asmFile.write("L"+str(quad)+":\n")
		loadvr(quadList[quad][1], 1)
		loadvr(quadList[quad][1], 2)
		asmFile.write("	blt $t1, $t2, L"+quadList[quad][3]+"\n")
	elif(quadList[quad][0] == ">="):
		asmFile.write("L"+str(quad)+":\n")
		loadvr(quadList[quad][1], 1)
		loadvr(quadList[quad][1], 2)
		asmFile.write("	bge $t1, $t2, L"+quadList[quad][3]+"\n")
	elif(quadList[quad][0] == "<="):
		asmFile.write("L"+str(quad)+":\n")
		loadvr(quadList[quad][1], 1)
		loadvr(quadList[quad][1], 2)
		asmFile.write("	ble $t1, $t2, L"+quadList[quad][3]+"\n")
	#operators
	elif(quadList[quad][0] == "+"):
		asmFile.write("L"+str(quad)+":\n")
		loadvr(quadList[quad][1], 1)
		loadvr(quadList[quad][1], 2)
		asmFile.write("	add $t1, $t1, $t2\n")
		storerv(3, quadList[quad][3])
	elif(quadList[quad][0] == "-"):
		asmFile.write("L"+str(quad)+":\n")
		loadvr(quadList[quad][1], 1)
		loadvr(quadList[quad][1], 2)
		asmFile.write("	sub $t1, $t1, $t2\n")
		storerv(3, quadList[quad][3])
	elif(quadList[quad][0] == "*"):
		asmFile.write("L"+str(quad)+":\n")
		loadvr(quadList[quad][1], 1)
		loadvr(quadList[quad][1], 2)
		asmFile.write("	mul $t1, $t1, $t2\n")
		storerv(3, quadList[quad][3])
	elif(quadList[quad][0] == "/"):
		asmFile.write("L"+str(quad)+":\n")
		loadvr(quadList[quad][1], 1)
		loadvr(quadList[quad][1], 2)
		asmFile.write("	div $t1, $t1, $t2\n")
		storerv(3, quadList[quad][3])
	#jump
	elif(quadList[quad][0] == "jump"):
		asmFile.write("L"+str(quad)+":\n")
		asmFile.write("	b L"+quadList[quad][3]+"\n")
	#assignment
	elif(quadList[quad][0] == ":="):
		asmFile.write("L"+str(quad)+":\n")
		loadvr(quadList[quad][1], 1)
		storerv(1, quadList[quad][3])
	#output
	elif(quadList[quad][0] == "out"):
		asmFile.write("L"+str(quad)+":\n")
		asmFile.write("	li $v0, 1\n")
		loadvr(quadList[quad][1], 2)
		asmFile.write("	move $a0, $t0\n")
		asmFile.write("	syscall\n")
	#input
	#Important!! If we have an input we have to remember to write a integer within the [-32767, 32767] range in mips as we execute the program otherwise the program will never finish
	elif(quadList[quad][0] == "inp"):
		asmFile.write("L"+str(quad)+":\n")
		asmFile.write("	li $v0, 5\n")
		asmFile.write("	syscall\n")
		asmFile.write("	move $t0, $v0\n")
		storerv(0, quadList[quad][1])
	#return
	elif(quadList[quad][0] == "retv"):
		asmFile.write("L"+str(quad)+":\n")
		loadvr(quadList[quad][1], 1)
		asmFile.write("	lw $t0, -8($sp)\n")
		asmFile.write("	sw $t1, ($t0)\n")
		asmFile.write("	lw $ra, ($sp)\n")
		asmFile.write("	jr $ra\n")
	#parameters
	elif(quadList[quad][0] == "par"):
		asmFile.write("L"+str(quad)+":\n")
		if(parSerialNum == 0):		#find the framelength of the function's/procedure's parameters
			for i in range(quad, quad+999):		#if we have a function/procedure with more that 999 parameters we may have a problem!!!
				if(quadList[i][0] == "call"):
					funcProc, nstLvl = searchEntity(quadList[i][1])
					break
			asmFile.write("	addi $fp, $sp, "+str(funcProc.framelength)+"\n")
		if(quadList[quad][2] == "CV"):
			loadvr(quadList[quad][1], 0)
			asmFile.write("	sw $t0, -"+str(12+4*parSerialNum)+"($fp)\n")
			parSerialNum+=1
		elif(quadList[quad][2] == "REF"):
			current_level = scopeList[-1].nestingLevel
			entity, nstLvl = searchEntity(quadList[quad][1])
			if(nstLvl == current_level and (entity.entityType == "Variable" or (entity.entityType == "Parameter" and entity.parMode == "in"))):		#variable or parameter passed by value
				asmFile.write("	addi $t0, $sp, -"+str(entity.offset)+"\n")
				asmFile.write("	sw $t0, -"+str(12+4*parSerialNum)+"($fp)\n")
			elif(nstLvl == current_level and entity.entityType == "Parameter" and entity.parMode == "inout"):	#parameter passed by reference
				asmFile.write("	lw $t0, -"+str(entity.offset)+"($sp)\n")
				asmFile.write("	sw $t0, -"+str(12+4*parSerialNum)+"($fp)\n")
			elif(nstLvl < current_level and (entity.entityType == "Variable" or (entity.entityType == "Parameter" and entity.parMode == "in"))):	#local variable or parameter passed by value on a lower nesting level
				gnvlcode(quadList[quad][1])
				asmFile.write("	sw $t0, -"+str(12+4*parSerialNum)+"($fp)\n")
			elif(nstLvl < current_level and entity.entityType == "Parameter" and entity.parMode == "inout"):	#parameter passed by reference on a lower nesting level
				gnvlcode(quadList[quad][1])
				asmFile.write("	lw $t0, ($t0)\n")
				asmFile.write("	sw $t0, -"+str(12+4*parSerialNum)+"($fp)\n")
			else:
				print("Error in assembly with a parameter by reference, in line "+str(line_num)+"!")
				sys.exit(-1)
			parSerialNum+=1
		elif(quadList[quad][2] == "RET"):
			funcProc, nstLvl = searchEntity(quadList[quad][1])
			asmFile.write("	addi $t0, $sp, -"+str(funcProc.offset)+"\n")
			asmFile.write("	sw $t0, -8($fp)\n")
	#functions or procedures
	elif(quadList[quad][0] == "call"):
		asmFile.write("L"+str(quad)+":\n")
		caller_entity, caller_nstLvl = searchEntity(name)				#nesting level of the caller(function/procedure/program we are in)
		called_entity, called_nstLvl = searchEntity(quadList[quad][1])	#nesting level of the called function/procedure
		if(caller_nstLvl == called_nstLvl):
			asmFile.write("	lw $t0, -4($sp)\n")
			asmFile.write("	sw $t0, -4($fp)\n")
		elif(caller_nstLvl < called_nstLvl):
			asmFile.write("	sw $sp, -4($fp)\n")
		asmFile.write("	addi $sp, $sp, "+str(called_entity.framelength)+"\n")
		asmFile.write("	jal L"+str(called_entity.startQuad) +"\n")
		asmFile.write("	addi $sp, $sp, -"+str(called_entity.framelength)+"\n")
		parSerialNum = 0	#reset parameters serial number for function/procedures in the same nesting level
	#begin/end/halt block
	elif(quadList[quad][0] == "begin_block" and quadList[quad][1] == program_name):	#for program
		asmFile.write("Lmain:\n")
		asmFile.write("L"+str(quad)+":\n")
		asmFile.write("	addi $sp, $sp, "+ str(programFramelength) +"\n")
		asmFile.write("	move $s0, $sp\n")
	elif(quadList[quad][0] == "begin_block" and quadList[quad][1] != program_name):	#for functions
		asmFile.write("L"+str(quad)+":\n")
		asmFile.write("	sw $ra, ($sp)\n")
	elif(quadList[quad][0] == "end_block" and quadList[quad][1] != program_name):	#for functions
		asmFile.write("L"+str(quad)+":\n")
		asmFile.write("	lw $ra, ($sp)\n")
		asmFile.write("	jr $ra\n")
	elif(quadList[quad][0] == "halt"):	#for program
		asmFile.write("L"+str(quad)+":\n")
		asmFile.write("	li $v0, 10 \n	syscall")
	else:
		print("Error: Invalid quad form attempted to assemble in mips!")
		sys.exit(1)
		
		



##################
#LEXICAL ANALYZER#
##################
def lex():
	global token, tokenID, state, line_num, buffer, counter, lookAhead_flag, c, f, OK, error
	#initialize/clear values
	state = 0 
	counter = 0
	buffer = list()	#clear buffer
	while(state!=OK and state!=error):
		#reads next character
		if(lookAhead_flag == True):	#checks if we had looked ahead previewsly
			char = c
			lookAhead_flag = False
		else:
			char = f.read(1)
		#states
		if(state==0):	#state0
			if(char in whitespaces):
				if(char=='\n'):
					line_num+=1
			elif(char in letters):
				state = 1
				counter+=1
				buffer.append(char)
			elif(char in numbers):
				state = 2
				buffer.append(char)
			elif(char=='+' or char=='-' or char=='*' or char=='/' or char=='='):
				if(char == '/'):	#check for comments
					c=f.read(1)
					lookAhead_flag = True
					if(c=='/' or c=='*'):
						state = 6
					else:
						token = char
						tokenID = char
						state = OK
				elif(char == '*'):	#check for comments ending without start
					c=f.read(1)
					lookAhead_flag = True
					if(c == '/'):
						print("Error line "+str(line_num)+": End of comments without starting point!")
						sys.exit(1)
					else:
						token = char
						tokenID = char
						state = OK
				else:				#just symbol
					token = char
					tokenID = char
					state = OK
			elif(char == '<'):
				state = 3
			elif(char == '>'):
				state = 4
			elif(char == ':'):
				state = 5
			elif(char==',' or char==';' or char==')' or char=='(' or char=='{' or char=='}' or char=='[' or char==']'):
				token = char
				tokenID = char
				state = OK
			elif(char==''):
				token = ''
				tokenID = 'EOF'
				state = OK
			elif(not(char in whitespaces or char in letters or char in numbers or char in specialChar)):
				print("Invalid character in line "+str(line_num)+". Compiler terminated!")
				state = error
				sys.exit(1)
		elif(state == 1):	#state1
			if(char in letters or char in numbers):
				if(counter<=30): #tokenize only the first 30 letters
					state = 1
					counter+=1
					buffer.append(char)
				else:
					state = 1
					counter+=1
			elif(char in whitespaces or char in specialChar):
				state = OK
				token = ''.join(buffer)
				if(token in bindedWords):
					tokenID = token + 'tk'
				else:
					tokenID = 'idtk'
				c = char
				lookAhead_flag = True
			elif(char == ''):
				state = OK
				tokenID = 'EOF'
			else:
				print("Invalid character(in string) in line "+str(line_num)+". Compiler terminated!")
				state = error
				sys.exit(1)
		elif(state == 2): 	#state2
			if(char in whitespaces or char in specialChar):
				token = ''.join(buffer)
				tokenID = 'consttk'
				state = OK
				c = char
				lookAhead_flag = True
			elif(char in numbers):
				buffer.append(char)
				token = ''.join(buffer)
				if(abs(int(token))>32767):
					state=error
					print("Constants must be within [-32767, 32767] range, line "+str(line_num)+". Program terminated!")
					sys.exit(-1)
			elif(char in letters):
				state=error
				print("Identifiers/Strings can't start with a digit, line "+str(line_num)+". Program terminated!")
				sys.exit(-1)
			else:
				print("Invalid character in number, line "+str(line_num)+". Compiler terminated!")
				state = error
				sys.exit(1)
		elif(state == 3):	#state3
			if(char == '='):
				token = '<='
				tokenID = '<='
				state = OK
			elif(char == ">"):
				token = '<>'
				tokenID = '<>'
				state = OK
			elif(char!='=' and char!='>'):
				token = '<'
				tokenID = '<'
				state = OK
				c = char
				lookAhead_flag = True
		elif(state == 4):	#state4
			if(char == '='):
				token = '>='
				tokenID = '>='
				state = OK
			elif(char!='='):
				token = '>'
				tokenID = '>'
				state = OK
				c = char
				lookAhead_flag = True
		elif(state == 5):	#state5
			if(char == '='):
				token = ':='
				tokenID = ':='
				state = OK
			elif(char!='='):
				token = ':'
				tokenID = ':'
				state = OK
				c = char
				lookAhead_flag = True
		elif(state == 6):	#state6
			if(char == '/'):	#line comments
				state = 7
			else:	#variable length comments
				state = 8
		elif(state == 7):	#state7
			if(char=='\n'):
				state = 0
			else:
				c = f.read(1)
				lookAhead_flag = True
				if((char=='/' and c=='/') or (char=='/' and c=='*') or (char=='*' and c=='/')):
					print("Error: Minimal++ cannot support nested comments, line "+str(line_num)+"!")
					sys.exit(1)
				state = 7
		elif(state == 8):	#state8
			if(char==''):	#check for EOF
				print("Error: File ended before comments could close, line "+str(line_num)+"!")
				state = error
				sys.exit(1)
			if(char!='*'):
				c = f.read(1)
				lookAhead_flag = True
				if((char=='/' and c=='/') or (char=='/' and c=='*')):
					print("Error: Minimal++ cannot support nested comments, line "+str(line_num)+"!")
					sys.exit(1)
				state = 8
			else:
				c = f.read(1)
				if(c!='/'):
					state = 8
				else:
					state = 0





#################
#SYNTAX ANALYZER#
#################
def program():
	addScope(0)
	lex()
	if(tokenID == 'programtk'):
		lex()
		if(tokenID == 'idtk'):
			global program_name
			program_name = token
			lex()
			if(tokenID == '{'):
				lex()
				block(program_name)
			else:
				print("Error1: missing '{' in line "+str(line_num)+"!")
				sys.exit(-1)
			if(tokenID != '}'):
				print("Error2: missing '}' in line "+str(line_num)+"!")
				sys.exit(-1)
			lex()	#Should terminate the program by returning EOF
		else:
			print("Error3: program name expected in line "+str(line_num)+"!")
			sys.exit(-1)
	else:
		print("Error4: the keyword 'program' was expected in line "+str(line_num)+"!")
		sys.exit(-1)

def block(name):
	global programFramelength, programStartQuad, parSerialNum
	parSerialNum = 0	#reset parameters serial number for function/procedures in different nesting levels
	funcProc = None
	declarations()
	subprograms()
	#startQuad initialized for every function/Procedure
	if not(name == program_name):
		funcProc, nestLvl = searchEntity(name)
		funcProc.startQuad = nextquad()
	genquad("begin_block", name)
	statements()
	if(name == program_name):
		genquad("halt")
	genquad("end_block", name)
	#we are creating the framelengths for program, functions and procedures
	scope = scopeList[-1]
	if not(len(scope.entityList) == 0):
		varPar = None
		for i in range(len(scope.entityList)-1, -1, -1):	
			if(scope.entityList[i].entityType == "Variable" or scope.entityList[i].entityType == "TempVariable" or scope.entityList[i].entityType == "Parameter"):
				varPar = scope.entityList[i]	#find the framelength of the last entity of the function/procedure
				break
		if not(varPar == None):
			if(name == program_name):
				programFramelength = varPar.offset+4		#last function's/procedure's entity framelength+4
				scope.framelength = programFramelength		#store scopes framelength
			else:
				funcProc.framelength = varPar.offset+4		#last function's/procedure's entity framelength+4
				scope.framelength = funcProc.framelength 	#store scopes framelength
	else:
		funcProc.framelength = 12
		scope.framelength = funcProc.framelength
	print("###BEFORE DELETION###")
	printScopeList()
	if(funcProc == None):
		quad = programStartQuad		#programs starting quad
		while(1):
			if(quadList[quad][0] == "halt"):
				create_assembly_file(quad, program_name)
				break;
			create_assembly_file(quad, program_name)	#arguments are the quad we are working on(key of dictionary quadList) and the functions/procedures name we are in
			quad+=1
	else:
		quad = int(funcProc.startQuad)		#the quad that the function/procedure will start(quadList key)
		while(1):
			if(quadList[quad][0] == "end_block"):
				create_assembly_file(quad, funcProc.name)
				programStartQuad = quad+1	#stores the quad that the program will start
				break;
			create_assembly_file(quad, funcProc.name)	#arguments are the quad we are working on(key of dictionary quadList) and the functions/procedures name we are in
			quad+=1
	if not(name == program_name):	#delete all but the 0 nesting level scopes
		deleteScope()				#because we need 0 nesting level for c code creation
		print("###AFTER DELETION###")
		printScopeList()
		print("####################################################################################")
	else:
		print("END OF SYMBOL TABLE!")

def declarations():
	while(tokenID == 'declaretk'):
		lex()
		varlist()
		scope = scopeList[-1]
		tempList = []	
		for entity in scope.entityList:
			tempList.append(entity.name)
		if not(len(tempList) == len(set(tempList))):
			print("Error: Duplicated variable name declared on the same function/procedure in line "+str(line_num)+"!")
			sys.exit(1)
		del tempList
		if(tokenID == ';'):
			lex()
		else:
			print("Error5: Symbol ';' was expected in line "+str(line_num)+"!")
			sys.exit(-1)

def varlist():
	if(tokenID == 'idtk'):
		offset = scopeList[-1].framelength
		addVariable(token, "Variable", offset, scopeList[-1].entityList)
		scopeList[-1].framelength = scopeList[-1].entityList[-1].offset+4
		lex()
		while(tokenID == ','):
			lex()
			if(tokenID == 'idtk'):
				offset = scopeList[-1].framelength
				addVariable(token, "Variable", offset, scopeList[-1].entityList)
				scopeList[-1].framelength = scopeList[-1].entityList[-1].offset+4
				lex()
			else:
				print("Error6: Identifier expected after ',' not '"+ token+"' in line "+str(line_num)+"!")
				sys.exit(-1)

def subprograms():
	while(tokenID == 'functiontk' or tokenID == 'proceduretk'):
		subprogram()

def subprogram():
	eType = tokenID
	lex()
	if(tokenID == 'idtk'):
		function_name = token
		if(eType == 'functiontk'):
			addFunction(function_name, "Function", scopeList[-1].entityList)
		else:
			addProcedure(function_name, "Procedure", scopeList[-1].entityList)
		scope = scopeList[-1]
		entity = scope.entityList[-1]
		for i in range(len(scope.entityList)-1):
			if(scope.entityList[i].name == entity.name):
				print("Error: Duplicated name of "+entity.entityType+" with a variable in the same scope, line "+str(line_num)+"!")	
				#you can't name a function/procedure with the same name as a declaration, function or procedure in the same scope
				sys.exit(1) 
		addScope(scopeList[-1].nestingLevel+1)
		lex()
		funcbody(function_name)
	else:
		print("Error7: Expected function or procedure identifier in line "+str(line_num)+"!")
		sys.exit(-1)

def funcbody(funcName):
	formalpars()
	if(tokenID == '{'):
		lex()
		block(funcName)
	else:
		print("Error8: missing '{' in line "+str(line_num)+"!")
		sys.exit(-1)
	if(tokenID != '}'):
		print("Error9: missing '}' in line "+str(line_num)+"!")
		sys.exit(-1)
	lex()

def formalpars():
	if(tokenID == '('):
		lex()
		formalparlist()
	else:
		print("Error10: missing '(' in line "+str(line_num)+"!")
		sys.exit(-1)
	if(tokenID != ')'):
		print("Error11: missing ')' in line "+str(line_num)+"!")
		sys.exit(-1)
	lex()
	
def formalparlist():
	if not(tokenID == ')'):
		formalparitem()
		while(tokenID == ','):
			lex()
			formalparitem()

def formalparitem():
	if(tokenID == 'intk'):
		arg = addArgument(token, scopeList[-2].entityList[-1].argumentList)
		lex()
		if(tokenID == 'idtk'):
			offset = scopeList[-1].framelength
			addParameter(token, "Parameter", arg.mode, offset, scopeList[-1].entityList)
			scopeList[-1].framelength = scopeList[-1].entityList[-1].offset+4
			lex()
		else:
			print("Error12: Identifier(name) of variables expected instead of '"+token+"' after 'in' in line "+str(line_num)+"!")
			sys.exit(1)
	elif(tokenID == 'inouttk'):
		arg = addArgument(token, scopeList[-2].entityList[-1].argumentList)
		lex()
		if(tokenID == 'idtk'):
			offset = scopeList[-1].framelength
			addParameter(token, "Parameter", arg.mode, offset, scopeList[-1].entityList)
			scopeList[-1].framelength = scopeList[-1].entityList[-1].offset+4
			lex()
		else:
			print("Error13: Identifier(name) of variables expected instead of '"+token+"' after 'inout' in line "+str(line_num)+"!")
			sys.exit(1)
	else:
		print("Error14: 'in' or 'inout' expected instead of '"+token+"' in line "+str(line_num)+"!")
		sys.exit(1)

def statements():
	if(tokenID != '{'):
		statement()
	elif(tokenID == '{'):
		lex()
		statement()
		while(tokenID == ';'):
			lex()
			statement()
		if(tokenID != '}'):
			print("Error15: missing '}' in line "+str(line_num)+"!")
			sys.exit(-1)
		lex()	

def statement():
	if(tokenID == 'idtk'):
		assignment_stat()
	elif(tokenID == 'iftk'):
		if_stat()
	elif(tokenID == 'whiletk'):
		while_stat()
	elif(tokenID == 'doublewhiletk'):
		doublewhile_stat()
	elif(tokenID == 'looptk'):
		loop_stat()
	elif(tokenID == 'exittk'):
		exit_stat()
	elif(tokenID == 'forcasetk'):
		forcase_stat()
	elif(tokenID == 'incasetk'):
		incase_stat()
	elif(tokenID == 'calltk'):
		call_stat()
	elif(tokenID == 'returntk'):
		return_stat()
	elif(tokenID == 'inputtk'):
		input_stat()
	elif(tokenID == 'printtk'):
		print_stat()

def assignment_stat():
	idname = token
	lex()
	if(tokenID == ':='):
		lex()
		exp = expression()
		genquad(":=", exp, "_", idname)
	else:
		print("Error16: ':=' expected instead of '"+token+"' in line "+str(line_num)+"!")
		sys.exit(1)

def if_stat():
	lex()
	if(tokenID == '('):
		lex()
		[Btrue, Bfalse] = condition()
	else:
		print("Error17: missing '(' in line "+str(line_num)+"!")
		sys.exit(-1)
	if(tokenID != ')'):
		print("Error18: missing ')' in line "+str(line_num)+"!")
		sys.exit(-1)
	lex()
	if(tokenID != 'thentk'):
		print("Error19: 'then' was expected instead of '"+token+"' in line "+str(line_num)+"!")
		sys.exit(-1)
	backpatch(Btrue, nextquad())
	lex()
	statements()
	ifList = makelist(nextquad())
	genquad("jump")
	backpatch(Bfalse, nextquad())
	elsepart()
	backpatch(ifList, nextquad())

def elsepart():
	if(tokenID == 'elsetk'):
		lex()
		statements()

def while_stat():
	lex()
	Bquad = nextquad()
	if(tokenID == '('):
		lex()
		[Btrue, Bfalse] = condition()
	else:
		print("Error20: missing '(' in line "+str(line_num)+"!")
		sys.exit(-1)
	if(tokenID != ')'):
		print("Error21: missing ')' in line "+str(line_num)+"!")
		sys.exit(-1)
	lex()
	backpatch(Btrue, nextquad())
	statements()
	genquad("jump", "_", "_", Bquad)
	backpatch(Bfalse, nextquad())

def doublewhile_stat():
	lex()
	if(tokenID == '('):
		lex()
		condition()
	else:
		print("Error22: missing '(' in line "+str(line_num)+"!")
		sys.exit(-1)
	if(tokenID != ')'):
		print("Error23: missing ')' in line "+str(line_num)+"!")
		sys.exit(-1)
	lex()
	statements()
	if(tokenID != 'elsetk'):
		print("Error24: 'else' was expected instead of '"+token+"' in line "+str(line_num)+"!")
		sys.exit(-1)
	lex()
	statements()

def loop_stat():
	lex()
	statements()

def exit_stat():
	lex()

def forcase_stat():
	lex()
	Fquad = nextquad()
	exitlist = emptylist()
	while(tokenID == 'whentk'):
		lex()
		if(tokenID == '('):
			lex()
			[condTrue, condFalse] = condition()
		else:
			print("Error25: missing '(' in line "+str(line_num)+"!")
			sys.exit(-1)
		if(tokenID != ')'):
			print("Error26: missing ')' in line "+str(line_num)+"!")
			sys.exit(-1)
		lex()
		if(tokenID != ':'):
			print("Error27: missing ':' in line "+str(line_num)+"!")
			sys.exit(-1)
		backpatch(condTrue, nextquad())
		lex()
		statements()
		Flist = makelist(nextquad())
		genquad("jump")
		exitlist = merge(exitlist, Flist)
		backpatch(condFalse, nextquad())
	if(tokenID != 'defaulttk'):
		print("Error28: 'default' was expected instead of '"+token+"' in line "+str(line_num)+"!")
		sys.exit(-1)
	lex()
	if(tokenID != ':'):
		print("Error29: missing ':' in line "+str(line_num)+"!")
		sys.exit(-1)
	lex()
	statements()
	backpatchQuad = str(int(nextquad())+1)
	backpatch(exitlist, backpatchQuad)
	exitQuad = str(int(nextquad())+2)
	genquad("jump", "_", "_", exitQuad)
	genquad("jump", "_", "_", Fquad)

def incase_stat():
	lex()
	while(tokenID == 'whentk'):
		lex()
		if(tokenID == '('):
			lex()
			condition()
		else:
			print("Error30: missing '(' in line "+str(line_num)+"!")
			sys.exit(-1)
		if(tokenID != ')'):
			print("Error31: missing ')' in line "+str(line_num)+"!")
			sys.exit(-1)
		lex()
		if(tokenID != ':'):
			print("Error32: missing ':' in line "+str(line_num)+"!")
			sys.exit(-1)
		lex()
		statements()

def return_stat():
	lex()
	exp = expression()
	genquad("retv", exp)

def call_stat():		
	lex()
	if(tokenID == 'idtk'):
		call_name = token
		#code that checks the right calling of a Procedure
		entity, nstLvl = searchEntity(call_name)
		argList = []
		if(entity.entityType == "Procedure"):
			for arg in entity.argumentList:
				argList.append(arg.mode)
		lex()
		actualpars(argList)
		genquad("call", call_name)
	else:
		print("Error33: Identifier of a procedures name was expected instead of '"+token+"' in line "+str(line_num)+"!")
		sys.exit(1)

def print_stat():
	lex()
	if(tokenID == '('):
		lex()
		exp = expression()
		genquad("out", exp)
	else:
		print("Error34: missing '(' in line "+str(line_num)+"!")
		sys.exit(-1)
	if(tokenID != ')'):
		print("Error35: missing ')' in line "+str(line_num)+"!")
		sys.exit(-1)
	lex()

def input_stat():
	lex()
	if(tokenID == '('):
		lex()
		inputID = token
		if(tokenID == 'idtk'):
			genquad("inp", inputID)
			lex()
		else:
			print("Error36: Input(from keyboard) identifier was expected instead of '"+token+"' in line "+str(line_num)+"!")
			sys.exit(1)
	else:
		print("Error37: missing '(' in line "+str(line_num)+"!")
		sys.exit(-1)
	if(tokenID != ')'):
		print("Error38: missing ')' in line "+str(line_num)+"!")
		sys.exit(-1)
	lex()

def actualpars(argList):
	#argList is a list that contains the arguments that a calling function/procedure is assigned
	#actual_argList is a list that contains the arguments that the function/procedure we called actually defined when we created it
	if(tokenID == '('):
		lex()
		actual_argList = actualparlist()
		if(argList != actual_argList):
			print("Error: Arguments assigned for this function/procedure are different from the ones we defined it with, in line "+str(line_num)+"!")
			sys.exit(1)
	else:
		print("Error39: missing '(' in line "+str(line_num)+"!")
		sys.exit(-1)
	if(tokenID != ')'):
		print("Error40: missing ')' in line "+str(line_num)+"!")
		sys.exit(-1)
	lex()

def actualparlist():
	actual_argList = []
	if not(tokenID == ')'):
		a = actualparitem()
		actual_argList.append(a)
		while(tokenID == ','):
			lex()
			a = actualparitem()
			actual_argList.append(a)
	return actual_argList

def actualparitem():
	argType = ""
	if(tokenID == 'intk'):
		argType = "in"
		lex()
		par_item = expression()
		genquad("par", par_item, "CV")
	elif(tokenID == 'inouttk'):
		argType = "inout"
		lex()
		if(tokenID == 'idtk'):
			par_item = token
			genquad("par", par_item, "REF")
			lex()
		else:
			print("Error41: Identifier(name) of variable was expected instead of '"+token+"' in line "+str(line_num)+"!")
			sys.exit(1)
	else:
		print("Error42: Parameter type('in' or 'inout') expected instead of '"+token+"' in line "+str(line_num)+"!")
		sys.exit(1)
	return argType

def condition():
	[Q1true, Q1false] = boolterm()
	Btrue = Q1true
	Bfalse = Q1false
	while(tokenID == 'ortk'):
		backpatch(Bfalse, nextquad())
		lex()
		[Q2true, Q2false] = boolterm()
		Btrue = merge(Btrue, Q2true)
		Bfalse = Q2false
	return [Btrue, Bfalse]

def boolterm():
	[R1true, R1false] = boolfactor()
	Qtrue = R1true
	Qfalse = R1false
	while(tokenID == 'andtk'):
		backpatch(Qtrue, nextquad())
		lex()
		[R2true, R2false] = boolfactor()
		Qfalse = merge(Qfalse, R2false)
		Qtrue = R2true
	return [Qtrue, Qfalse]

def boolfactor():
	if(tokenID == 'nottk'):
		lex()
		if(tokenID == '['):
			lex()
			[Btrue, Bfalse] = condition()
		else:
			print("Error43: missing '[' in line "+str(line_num)+"!")
			sys.exit(-1)
		if(tokenID != ']'):
			print("Error44: missing ']' in line "+str(line_num)+"!")
			sys.exit(-1)
		Rtrue = Bfalse
		Rfalse = Btrue
		lex()
	elif(tokenID == '['):
		lex()
		[Btrue, Bfalse] = condition()
		if(tokenID != ']'):
			print("Error45: missing ']' in line "+str(line_num)+"!")
			sys.exit(-1)
		Rtrue = Btrue
		Rfalse = Bfalse
		lex()
	else:
		exp1 = expression()
		relop = relational_oper()
		exp2 = expression()
		Rtrue = makelist(nextquad())
		genquad(relop, exp1, exp2)
		Rfalse = makelist(nextquad())
		genquad("jump")
	return [Rtrue, Rfalse]


def expression():
	opsign = optional_sign()
	t1 = term()
	if(opsign == '+' or opsign == '-'):
		t1 = opsign + t1
	while(tokenID == '+' or tokenID == '-'):
		oper = token
		add_oper()
		t2 = term()
		w = newtemp()
		genquad(oper, t1, t2, w)
		t1 = w
	return t1

def term():
	f1 = factor()
	while(tokenID == '*' or tokenID == '/'):
		oper = token
		mul_oper()
		f2 = factor()
		w = newtemp()
		genquad(oper, f1 ,f2 , w)
		f1 = w
	return f1

def factor():
	factor_value = token
	if(tokenID == 'consttk'):
		lex()
	elif(tokenID == '('):
		lex()
		exp = expression()
		factor_value = exp
		if(tokenID != ')'):
			print("Error46: missing ')' in line "+str(line_num)+"!")
			sys.exit(-1)
		lex()
	elif(tokenID == 'idtk'):
		lex()
		#code that checks the right calling of a Function
		entity, nstLvl = searchEntity(factor_value)
		argList = []
		if(entity.entityType == "Function"):
			for arg in entity.argumentList:
				argList.append(arg.mode)
		function_result = idtail(argList)
		#code that checks the right creation of a Function
		if(function_result == True):
			if not(entity.entityType == "Function"):
				print("Error: '"+entity.name+"' is not a function, line "+str(line_num)+"!")
				sys.exit(1)
			w = newtemp()
			genquad("par", w, "RET")
			genquad("call", factor_value)
			factor_value = w
		else:
			if(entity.entityType == "Function" or entity.entityType == "Procedure"):
				print("Error: '"+entity.name+"' is not a variable, line "+str(line_num)+"!")
				sys.exit(1)
	else:
		print("Error47: Constant or '(' or identifier missing in factor in line "+str(line_num)+"!")
		sys.exit(1)
	return factor_value

def idtail(argList):
	function_flag = False
	if(tokenID == '('):	
		actualpars(argList)
		function_flag = True
	return function_flag

def relational_oper():
	relop = token
	if(tokenID == '='):
		lex()
	elif(tokenID == '<='):
		lex()
	elif(tokenID == '>='):
		lex()
	elif(tokenID == '>'):
		lex()
	elif(tokenID == '<'):
		lex()
	elif(tokenID == '<>'):
		lex()
	else:
		print("Error48: "+token+" causes an error in line "+str(line_num)+".Relational operator expected!")
		sys.exit(-1)
	return relop

def add_oper():
	if(tokenID == '+'):
		lex()
	elif(tokenID == '-'):
		lex()
	else:
		print("Error49: "+token+" causes an error in line "+str(line_num)+".Addition operator expected!")
		sys.exit(-1)

def mul_oper():
	if(tokenID == '*'):
		lex()
	elif(tokenID == '/'):
		lex()
	else:
		print("Error50: "+token+" causes an error in line "+str(line_num)+".Multiplier operator expected!")
		sys.exit(-1)

def optional_sign():
	sign = token
	if(tokenID == '+' or tokenID == '-'):
		add_oper()
	return sign





################
#MAIN/Open file#
################
if(len(sys.argv)!=2):
	print("Error: Expecting file name")
	print("Try: python compiler.py *.min")
	sys.exit(1)
f = open(sys.argv[1],'r')	#opens .min file
fname = sys.argv[1].split(".").pop(0)	#keeps the name of the file that we compile e.g test.min --> test
#assembly file
asmFile = open(fname+".asm", "w")
asmFile.write("	b Lmain\n")
#create_assembly_file()
program()
f.close()
#int file
intFile = open(fname+".int", "w")
create_int_file()
intFile.close()
#c file
cFile = open(fname+".c", "w")
create_c_file()
cFile.close()
#close asmFile and terminate compiler.py
asmFile.close()
sys.exit(0)

#IMPORTANT NOTE!
#Only lexical and syntax code for doublewhile_stat(), loop_stat(), exit_stat() and incase_stat()