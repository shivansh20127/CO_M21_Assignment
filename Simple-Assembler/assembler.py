import sys
from input import *
from variables import *
FLAGS={"V":0,"L":0,"G":0,"E":0}
R_addr={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
R_val={"R0":0,"R1":0,"R2":0,"R3":0,"R4":0,"R5":0,"R6":0}
Register=["R0","R1","R2","R3","R4","R5","R6"]				#Registers_Name
flag=False
flag_index=0
error_index=0
i=0
#******************************************************************************************************

def perform_add(instruc):
	global flag
	global flag_index
	global error_index
	global i
	if((len(instruc) != 4) or (instruc[1] not in Register) or (instruc[2] not in Register) or (instruc[3] not in Register)):
		print("Error at : line",str(error_index),"Addition Instruction is Invalid !")
		return 
	else:
		answer=R_val[instruc[2]]+R_val[instruc[3]]
		if(answer>=2**16):
			R_val[instruc[1]]=answer%(2**16)
			FLAGS["V"]=1
			flag=True
			flag_index=i
		else:
			R_val[instruc[1]]=answer
		ans= "00000"+"00"+R_addr[instruc[1]]+R_addr[instruc[2]]+R_addr[instruc[3]]
		print(ans)

def perform_sub(instruc):
	global flag
	global flag_index
	global error_index
	global i
	if((len(instruc) != 4) or (instruc[1] not in Register) or (instruc[2] not in Register) or (instruc[3] not in Register)):
		print("Error at : line",str(error_index),"Subtraction Instruction is invalid !")
		return
	else:
		answer=R_val[instruc[2]]-R_val[instruc[3]]
		if(answer<0):
			R_val[instruc[1]]=0
			FLAGS["V"]=1
			flag=True
			flag_index=i
		else:
			R_val[instruc[1]]=answer
		ans= "00001"+"00"+R_addr[instruc[1]]+R_addr[instruc[2]]+R_addr[instruc[3]]
		print(ans)

def perform_mov_imm(instruc):
	global error_index
	if((len(instruc)!=3) or (instruc[1] not in Register)):
		print("Error at : line",str(error_index),"Move Immediate instruction is invalid !")
		return
	else:
		imm=instruc[2][1:]
		imm_val=int(imm)
		if(imm_val>255 or imm_val<0):
			print("Error at : line",str(error_index),"Move Immediate Instruction is Invalid !")
			return 
		R_val[instruc[1]]=int(imm)
		bin_val=bin(int(imm)).replace("0b", "")
		bin_val="0"*(8-len(bin_val))+bin_val
		ans= "00010"+R_addr[instruc[1]]+bin_val
		print(ans)

def perform_mov_reg(instruc):
	global error_index
	if(len(instruc)!=3):
		print("Error at : line",str(error_index),"Move Register instruction is Invalid !")
		return
	if(((instruc[1] not in Register) or (instruc[2] not in Register)) and (instruc[2]!="FLAGS")):
		print("Error at : line",str(error_index),"Move Register instruction is Invalid !")
		return
	elif(instruc[2]=="FLAGS"):
		bin_ans=int(str(FLAGS["V"])+str(FLAGS["L"])+str(FLAGS["G"])+str(FLAGS["E"]),2)
		R_val[instruc[1]]=bin_ans
		ans="00011"+"00000"+R_addr[instruc[1]]+R_addr[instruc[2]]
		print(ans) 
	else:
		R_val[instruc[1]]=R_val[instruc[2]]
		ans= "00011"+"00000"+R_addr[instruc[1]]+R_addr[instruc[2]]
		print(ans)

def perform_load(instruc):
	global error_index
	if(len(instruc)!=3):
		print("Error at : line",str(error_index),"Load instruction is Invalid !")
		return
	if(instruc[1] not in Register or instruc[2] not in var):
		print("Error at : line",str(error_index),"Load instruction is Invalid !")
		return  
	else:
		R_val[instruc[1]]=var[instruc[2]]
		bin_val=bin(int(var[instruc[2]])).replace("0b", "")
		ans= "00100"+R_addr[instruc[1]]+"0"*(8-len(bin_val))+bin_val
		print(ans)

def perform_store(instruc):
	global error_index
	if(len(instruc)!=3):
		print("Error at : line",str(error_index),"Store Instruction is invalid !")
		return
	if((instruc[1] not in Register) or (instruc[2] not in var)):
		print("Error at : line",str(error_index),"Store instruction is Invalid !")
		return 
	else:
		bin_val=bin(int(var[instruc[2]])).replace("0b", "")
		var[instruc[2]]=R_val[instruc[1]]
		ans= "00101"+R_addr[instruc[1]]+"0"*(8-len(bin_val))+bin_val
		print(ans)

def perform_multiply(instruc):
	global error_index
	global flag
	global flag_index
	global i
	if((len(instruc) != 4) or (instruc[1] not in Register) or (instruc[2] not in Register) or (instruc[3] not in Register)):
		print("Error at : line",str(error_index),"Multiplication Instruction is invalid !")
		return
	else:
		answer=R_val[instruc[2]]*R_val[instruc[3]]
		if(answer>=2**16):
			R_val[instruc[1]]=answer%2**16
			FLAGS["V"]=1
			flag=True
			flag_index=i
		else:
			R_val[instruc[1]]=answer
		ans= "00110"+"00"+R_addr[instruc[1]]+R_addr[instruc[2]]+R_addr[instruc[3]]
		print(ans)

def perform_divide(instruc):
	global error_index
	if((len(instruc) != 3) or (instruc[1] not in Register) or (instruc[2] not in Register)):
		print("Error at : line",str(error_index),"Division Instruction is invalid !")
		return
	else:
		try:
			R_val["R0"]=R_val[instruc[1]]//R_val[instruc[2]]
			R_val["R1"]=R_val[instruc[1]]%R_val[instruc[2]]
			ans= "00111"+"00000" + R_addr[instruc[1]] + R_addr[instruc[2]]
			print(ans)
		except ZeroDivisionError as e:
			print("Error at : line",str(error_index),"Error: ",e,": Hence division cannot be performed") 

def perform_right_shift(instruc):
	global error_index
	if(len(instruc)!=3):
		print("Error at : line",str(error_index),"Right Shift Instruction is Invalid !")
		return
	elif(instruc[2][0]!="$" or (instruc[1] not in Register)):
		print("Error at : line",str(error_index),"Right Shift Instruction is Invalid !")
		return
	else:
		imm=instruc[2][1:]
		imm_val=int(imm)
		if(imm_val>255 or imm_val<0):
			print("Error at : line",str(error_index),"Right Shift Instruction is Invalid !")
			return
		R_val[instruc[1]]=R_val[instruc[1]]>>int(imm)
		bin_val=bin(int(imm)).replace("0b", "")
		bin_val="0"*(8-len(bin_val))+bin_val
		ans= "01000"+R_addr[instruc[1]]+bin_val
		print(ans)

def perform_left_shift(instruc):
	global error_index
	if(len(instruc)!=3):
		print("Error at : line",str(error_index),"Left Shift Instruction is Invalid !")
		return
	elif(instruc[2][0]!="$" or (instruc[1] not in Register)):
		print("Error at : line",str(error_index),"Left Shift Instruction is Invalid !")
	else:
		imm=instruc[2][1:]
		imm_val=int(imm)
		if(imm_val>255 or imm_val<0):
			print("Error at : line",str(error_index),"Left Shift Instruction is Invalid !")
			return
		answer=R_val[instruc[1]]<<int(imm)
		bin_val=bin(int(imm)).replace("0b", "")
		if(answer>=2**16):
			R_val[instruc[1]]=answer%(2**16)
		else:
			R_val[instruc[1]]=answer
		bin_val="0"*(8-len(bin_val))+bin_val
		ans= "01001"+R_addr[instruc[1]]+bin_val
		print(ans)

def perform_xor(instruc):
	global error_index
	if(len(instruc)!=4 or (instruc[1] not in Register) or (instruc[2] not in Register) or (instruc[3] not in Register)):
		print("Error at : line",str(error_index),"Logical XOR Instruction is Invalid !")
		return
	else:
		R_val[instruc[1]]=R_val[instruc[2]]^R_val[instruc[3]]
		ans= "01010"+"00"+R_addr[instruc[1]]+R_addr[instruc[2]]+R_addr[instruc[3]]
		print(ans)

def perform_or(instruc):
	global error_index
	if(len(instruc)!=4 or (instruc[1] not in Register) or (instruc[2] not in Register) or (instruc[3] not in Register)):
		print("Error at : line",str(error_index),"Logical OR Instruction is Invalid !")
		return
	else:
		R_val[instruc[1]]=R_val[instruc[2]] | R_val[instruc[3]]
		ans= "01011"+"00"+R_addr[instruc[1]]+R_addr[instruc[2]]+R_addr[instruc[3]]
		print(ans)

def perform_and(instruc):
	global error_index
	if(len(instruc)!=4 or (instruc[1] not in Register) or (instruc[2] not in Register) or (instruc[3] not in Register)):
		print("Error at : line",str(error_index),"Logical AND Instruction is Invalid !")
		return
	else:
		R_val[instruc[1]]=R_val[instruc[2]] & R_val[instruc[3]]
		ans= "01100"+"00"+R_addr[instruc[1]]+R_addr[instruc[2]]+R_addr[instruc[3]]
		print(ans)

def invert(s):
    v=""
    for i in range (len(s)):
        if(s[i]=="0"):
            v=v+"1"
        else:
            v=v+"0"
    return(v)

def perform_inversion(instruc):
	global error_index
	if(len(instruc)!=3 or (instruc[1] not in Register) or (instruc[2] not in Register)):
		print("Error at : line",str(error_index),"Logical Invert Instruction is Invalid !")
		return
	else:
		bin_val=bin(int(R_val[instruc[2]])).replace("0b","")
		R_val[instruc[1]]=int(invert(bin_val),2)
		ans= "01101"+"00000"+R_addr[instruc[1]]+R_addr[instruc[2]]
		print(ans)

def perform_cmp(instruc):
	global i
	global error_index
	global flag
	global flag_index
	if(len(instruc)!=3 or (instruc[1] not in Register) or (instruc[2] not in Register)):
		print("Error at : line",str(error_index),"Compare Instruction is Invalid!")
		return 
	else:
		#Note: We will set the flag variable as 0 i.e. all flag values as zero
		if(R_val[instruc[1]]==R_val[instruc[2]]):
			FLAGS["E"]=1
			flag=True
			flag_index=i
		elif(R_val[instruc[1]]>R_val[instruc[2]]):
			FLAGS["G"]=1
			flag=True
			flag_index=i
		elif(R_val[instruc[1]]<R_val[instruc[2]]):
			FLAGS["L"]=1
			flag=True
			flag_index=i
		ans= "01110"+"00000"+R_addr[instruc[1]]+R_addr[instruc[2]]
		print(ans)

#******************************************************************************************************

def main2(instruc):
	global error_index
	if(instruc[0] == "add"):			#Addition
		perform_add(instruc)
	elif(instruc[0] == "sub"):			#Subtraction
		perform_sub(instruc)
	elif(instruc[0] == "mov"):			#Move 
		# .. here we have to do some work to differentiate between two move instructions .. 
		# .. and then we can perform the move operation ..
		if(instruc[2][0]=='$'):
			perform_mov_imm(instruc)
		else:
			perform_mov_reg(instruc)
	elif(instruc[0] == "ld"):			#Load the value 
		perform_load(instruc)
	elif(instruc[0] == "st"):			#Store the value
		perform_store(instruc)
	elif(instruc[0] == "mul"):			#Multiplication
		perform_multiply(instruc)
	elif(instruc[0] == "div"):			#Division
		perform_divide(instruc)
	elif(instruc[0]== "rs"):			#Right Shift
		perform_right_shift(instruc)
	elif(instruc[0]== "ls"):			#Left Shift
		perform_left_shift(instruc)
	elif(instruc[0] == "xor"):			#XOR operation 
		perform_xor(instruc)
	elif(instruc[0] == "or"):			#OR operation
		perform_or(instruc)
	elif(instruc[0] == "and"):			#AND operation
		perform_and(instruc)
	elif(instruc[0] == "not"):			#NOT operation
		perform_inversion(instruc)
	elif(instruc[0] == "cmp"):			#Compare the two values
		perform_cmp(instruc)
	else:
		print("Error at : line",str(error_index),"Invalid Instruction")

#******************************************************************************************************
def reset_flag():
	global i
	global flag
	global flag_index
	if(flag==True):
		if(flag_index==i-1):
			FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0
			flag=False
			flag_index=0

#******************************************************************************************************

def main():
	global label_dic
	global error_index
	global flag
	global i
	for i in range(len(list_of_instructions)):
		error_index=i+1
		instruc=list_of_instructions[i]
		if i in error_dupli:
			print("Error at : line",str(error_index),"Duplicate declaration")
			continue
		if i in error_var:
			print("Error at : line",str(error_index),"Invalid declaration of variable")
			continue

		elif(instruc[0] in label_dic or (instruc[0][len(instruc[0])-1])==":"):
			instruc=instruc[1:]	
		if(instruc==[]):
			print("Error at : line",str(error_index),"Empty Label")
			continue
		if(instruc[0] == "hlt"):			#Stops the machine from executing until reset
			#Taking Input of the next line to check whether hlt is at EOF or not
			if(i==(len(list_of_instructions)-1)):
				print("1001100000000000")
				sys.exit()					#Exits the program
			else:
				#Prints the error message
				print("Error at : line",str(error_index),"hlt not being used as the last instruction")
				sys.exit()					#Exits the program

		elif(instruc[0]=="var"):
			continue
		elif(instruc[0] == "jmp"):	
			if(len(instruc)!=2 or (instruc[1] not in label_dic)):
				print("Error at : line",str(error_index),"Unconditional Jump Instruction is Invalid !") 
			else:
				bin_val=bin(int(label_dic[instruc[1]])).replace("0b", "")
				ans="01111"+"000"+"0"*(8-len(bin_val))+bin_val
				print(ans)

		elif(instruc[0] == "jlt"):	
			if(len(instruc)!=2 or (instruc[1] not in label_dic)):
				print("Error at : line",str(error_index)," Jump if LESS than Instruction is Invalid !") 
			else:
				bin_val=bin(int(label_dic[instruc[1]])).replace("0b", "")
				ans="10000"+"000"+"0"*(8-len(bin_val))+bin_val
				print(ans)

		elif(instruc[0] == "jgt"):	
			if(len(instruc)!=2 or (instruc[1] not in label_dic)):
				print("Error at : line",str(error_index)," Jump if GREATER Than Instruction is Invalid !") 
			else:
				bin_val=bin(int(label_dic[instruc[1]])).replace("0b", "")
				ans="10001"+"000"+"0"*(8-len(bin_val))+bin_val
				print(ans)

		elif(instruc[0] == "je"):	
			if(len(instruc)!=2 or (instruc[1] not in label_dic)):
				print("Error at : line",str(error_index)," Jump if EQUAL To Instruction is Invalid !") 
			else:
				bin_val=bin(int(label_dic[instruc[1]])).replace("0b", "")
				ans="10010"+"000"+"0"*(8-len(bin_val))+bin_val
				print(ans)

		else:
			main2(instruc)  				#Calls the main2 function to perform the operations
		reset_flag()						#Resets the flag

#******************************************************************************************************

#Main entrance of the Code
if __name__=='__main__':
	main()		#Main function call