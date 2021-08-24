import sys
from input import *
from variable import *
global input_lis
FLAGS={"V":0,"L":0,"G":0,"E":0}								#Dictioary of all the Flag instructions
R_addr={"000":"R0","001":"R1","010":"R2","011":"R3","100":"R4","101":"R5","110":"R6","111":"FLAGS"}
R_val={"R0":0,"R1":0,"R2":0,"R3":0,"R4":0,"R5":0,"R6":0}	#Value in Register
Register=["R0","R1","R2","R3","R4","R5","R6"]				#Registers_Name
flag=False									#boolean variable to show flag is set or not
flag_index=0								#index of the line in which flag was set
i=0											#just a variable for iteration
cycle=0
Cycle_number=[]
memory_address_accessed=[]

def perform_add():
	global input_lis
	global i
	global flag
	global flag_index
	addr1=input_lis[1][7:10]
	addr2=input_lis[1][10:13]
	addr3=input_lis[1][13:16]
	FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0
	answer=R_val[R_addr[addr2]]+R_val[R_addr[addr3]]
	if(answer>=2**16):
		R_val[R_addr[addr1]]=answer%(2**16)
		FLAGS["V"]=1
		flag=True
		flag_index=i
	else:
		R_val[R_addr[addr1]]=answer

def perform_sub():
	global input_lis
	global i
	global flag
	global flag_index
	addr1=input_lis[1][7:10]
	addr2=input_lis[1][10:13]
	addr3=input_lis[1][13:16]
	answer=R_val[R_addr[addr2]]-R_val[R_addr[addr3]]
	FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0		
	if(R_val[R_addr[addr1]]<0):		#if value is less than zero, result =0
		R_val[R_addr[addr1]]=0
		FLAGS["V"]=1
		flag=True
		flag_index=i
	else:		
		R_val[R_addr[addr1]]=answer

def perform_mov_imm():
	global input_lis
	global i
	addr1=input_lis[1][5:8]
	value=int(input_lis[1][8:],2)
	R_val[R_addr[addr1]]=value
	FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0           


def perform_mov_reg():
	global input_lis
	global i
	addr1=input_lis[1][10:13]
	addr2=input_lis[1][13:16]
	if(addr2=="111"):
		bin_ans=int(str(FLAGS["V"])+str(FLAGS["L"])+str(FLAGS["G"])+str(FLAGS["E"]),2)
		R_val[R_addr[addr1]]=bin_ans
		FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0
		return
	R_val[R_addr[addr1]]=R_val[R_addr[addr2]]
	FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0           

	
def perform_load():
	global input_lis
	global i
	global memory_dump
	addr1=input_lis[1][5:8]
	memory_addr=int(input_lis[1][8:],2)
	R_val[R_addr[addr1]]=int(memory_dump[memory_addr],2)
	FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0           

def perform_store():
	global input_lis
	global i
	global memory_dump
	addr1=input_lis[1][5:8]
	memory_addr=int(input_lis[1][8:],2) 
	memory_dump[memory_addr]=bin(R_val[R_addr[addr1]])[2:].zfill(16)
	FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0           


def perform_multiply():
	global input_lis
	global i
	global flag
	global flag_index
	addr1=input_lis[1][7:10]
	addr2=input_lis[1][10:13]
	addr3=input_lis[1][13:16]
	FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0
	answer=R_val[R_addr[addr2]]*R_val[R_addr[addr3]]
	if(answer>=2**16):		#if answer is greater than range
		R_val[R_addr[addr1]]=answer%2**16
		FLAGS["V"]=1
		flag=True
		flag_index=i
	else:
		R_val[R_addr[addr1]]=answer
		
	
def perform_divide():
	global input_lis
	global i
	addr1=input_lis[1][10:13]
	addr2=input_lis[1][13:16]
	R_val["R0"]=R_val[R_addr[addr1]]//R_val[R_addr[addr2]]
	R_val["R1"]=R_val[R_addr[addr1]]%R_val[R_addr[addr2]]
	FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0           


def perform_right_shift():
	global input_lis
	global i
	addr1=input_lis[1][5:8]
	imm=int(input_lis[1][8:],2)
	R_val[R_addr[addr1]]=R_val[R_addr[addr1]]>>imm
	FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0           

	
def perform_left_shift():
	global input_lis
	global i
	pass
	addr1=input_lis[1][5:8]
	imm=int(input_lis[1][8:],2)
	R_val[R_addr[addr1]]=R_val[R_addr[addr1]]<<imm
	FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0           

	
def perform_xor():
	global input_lis
	global i
	addr1=input_lis[1][7:10]
	addr2=input_lis[1][10:13]
	addr3=input_lis[1][13:16]
	R_val[R_addr[addr1]]=R_val[R_addr[addr2]]^R_val[R_addr[addr3]]
	FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0           


def perform_or():
	global input_lis
	global i
	addr1=input_lis[1][7:10]
	addr2=input_lis[1][10:13]
	addr3=input_lis[1][13:16]
	R_val[R_addr[addr1]]=R_val[R_addr[addr2]]| R_val[R_addr[addr3]]
	FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0           

	
def perform_and():
	global input_lis
	global i
	addr1=input_lis[1][7:10]
	addr2=input_lis[1][10:13]
	addr3=input_lis[1][13:16]
	R_val[R_addr[addr1]]=R_val[R_addr[addr2]] & R_val[R_addr[addr3]]
	FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0           


def invert(s):
    v=""
    for i in range (len(s)):
        if(s[i]=="0"):
            v=v+"1"
        else:
            v=v+"0"
    return(v)

def perform_inversion():
	global input_lis
	global i
	addr1=input_lis[1][10:13]
	addr2=input_lis[1][13:16]
	ans=invert(bin(R_val[R_addr[addr2]])[2:].zfill(16))
	R_val[R_addr[addr1]]=int(ans,2)
	FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0           


def perform_cmp():
	global input_lis
	global i
	global flag
	global flag_index
	addr1=input_lis[1][10:13]
	addr2=input_lis[1][13:16]
	FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0           
	if(R_val[R_addr[addr1]]==R_val[R_addr[addr2]]):
		FLAGS["E"]=1
		flag=True
		flag_index=i
	elif(R_val[R_addr[addr1]]>R_val[R_addr[addr2]]):
		FLAGS["G"]=1
		flag=True
		flag_index=i
	elif(R_val[R_addr[addr1]]<R_val[R_addr[addr2]]):
		FLAGS["L"]=1
		flag=True
		flag_index=i


def main2():
	global input_lis
	if(input_lis[0] == "00000"):			#Addition
		perform_add()
	elif(input_lis[0] == "00001"):			#Subtraction
		perform_sub()
	elif(input_lis[0] == "00010"):			#Move 
		perform_mov_imm()
	elif (input_lis[0]=="00011"):
		perform_mov_reg()
	elif(input_lis[0] == "00100"):			#Load the value 
		perform_load()
	elif(input_lis[0] == "00101"):			#Store the value
		perform_store()
	elif(input_lis[0] == "00110"):			#Multiplication
		perform_multiply()
	elif(input_lis[0] == "00111"):			#Division
		perform_divide()
	elif(input_lis[0] == "01000"):			#Right Shift
		perform_right_shift()
	elif(input_lis[0] == "01001"):			#Left Shift
		perform_left_shift()
	elif(input_lis[0] == "01010"):			#XOR operation 
		perform_xor()
	elif(input_lis[0] == "01011"):			#OR operation
		perform_or()
	elif(input_lis[0] == "01100"):			#AND operation
		perform_and()
	elif(input_lis[0] == "01101"):			#NOT operation
		perform_inversion()
	elif(input_lis[0] == "01110"):			#Compare the two values
		perform_cmp()

def print_every_register():
	bin_val=bin(i).replace("0b", "")                                #PC printing
	bin_val="0"*(8-len(bin_val))+bin_val
	print(bin_val+" ",end="")
	for j in range(0,7):
		bin_val=bin(R_val[Register[j]]).replace("0b", "")       
		bin_val="0"*(16-len(bin_val))+bin_val
		print(bin_val+" ",end="")
	addr1=bin(FLAGS["V"]).replace("0b", "")
	addr2=bin(FLAGS["L"]).replace("0b", "")
	addr3=bin(FLAGS["G"]).replace("0b", "")
	addr4=bin(FLAGS["E"]).replace("0b", "")
	bin_val="0"*12+str(addr1)+str(addr2)+str(addr3)+str(addr4)
	print(bin_val,end="")
	print("")                                                       #empty line 

def bonus_graph():
	global Cycle_number			
	global cycle
	global memory_address_accessed
	Cycle_number.append(cycle)							#Adding cycle number to list
	memory_address_accessed.append(i)
	if(input_lis[0]=="00100" or input_lis[0]=="00101"): 
		Cycle_number.append(cycle)
		mem_accessed=int(input_lis[1][8:],2)
		memory_address_accessed.append(mem_accessed)
	cycle+=1

def printing():
	global memory_dump
	for loop_invariant in range(len(memory_dump)):
		print(memory_dump[loop_invariant])
	
def plot():
	from matplotlib import pyplot as plt
	plt.scatter(Cycle_number,memory_address_accessed,s=120,marker="o",color="red",edgecolor='black',linewidths=1.5,hatch='//////')
	plt.title=("Cycle vs Memory Address")
	plt.xlabel("Cycle Number")
	plt.ylabel("Memory Address Accessed")
	plt.show()

def main():
	global FLAGS
	global input_lis
	global i
	i=0
	while i<len(list_of_binary_instructions):
		input_lis=list_of_binary_instructions[i]
		if(input_lis[0]=="10011"):
			print_every_register()
			printing()
			plot()
			sys.exit();
		elif (input_lis[0]=="01111"):
			bonus_graph()
			print_every_register()
			i=int(input_lis[1][8:],2)
			FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0           
		elif(input_lis[0]=="10000"):
			if(FLAGS["L"]==1):
				FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0
				print_every_register()
				bonus_graph()
				i=int(input_lis[1][8:],2)
			else:
				FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0
				print_every_register()
				bonus_graph()
				i=i+1
		elif(input_lis[0]=="10001"):
			if(FLAGS["G"]==1):
				FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0	
				print_every_register()
				bonus_graph()
				i=int(input_lis[1][8:],2)
			else:
				FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0
				print_every_register()
				bonus_graph()
				i=i+1
		elif(input_lis[0]=="10010" ):
			if(FLAGS["E"]==1):
				FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0
				print_every_register()
				bonus_graph()
				i=int(input_lis[1][8:],2)
			else:
				FLAGS["V"]=FLAGS["G"]=FLAGS["E"]=FLAGS["L"]=0
				print_every_register()
				bonus_graph()
				i=i+1
		else:
			main2()
			print_every_register()
			bonus_graph()
			i=i+1

if __name__ == "__main__":
	main()

