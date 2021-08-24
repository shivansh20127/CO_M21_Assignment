from input import *
length_of_file=len(list_of_binary_instructions)
x=256-length_of_file
memory_dump=[]
for i in range(length_of_file):
	memory_dump.append(list_of_binary_instructions[i][1])
for i in range(x):
	memory_dump.append("0"*16)