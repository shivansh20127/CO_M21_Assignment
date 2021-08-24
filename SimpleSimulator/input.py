import os
lines = os.read(0, 10**6).strip().splitlines()  
list_of_binary_instructions=[]
for x in lines:
    line = x.decode('utf-8')
    temp_list=[line[0:5],line]  #breaking the opcode and the rest of the line
    if(temp_list!=[]):              #ignoring white spaces
        list_of_binary_instructions.append(temp_list)