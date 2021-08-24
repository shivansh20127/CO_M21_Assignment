from input import *
var={}
var_list=[]
label_list=[]
label_dic={}
error_var=[]
error_dupli=[]
counter=0
for i in range(len(list_of_instructions)):
	instruc=list_of_instructions[i]
	if(instruc[0]=="var"):
		if(len(instruc)==2):
			if(instruc[1] not in var_list):
				var[instruc[1]]=0
				var_list.append(instruc[1])
			else:
				error_dupli.append(i)
		else:
			error_var.append(i)
	else:
		if(instruc[0][len(instruc[0])-1]==":"):
			if(instruc[0][0:len(instruc[0])-1] not in label_list):
				label_dic[instruc[0][:len(instruc[0])-1]]=counter
				label_list.append(instruc[0][:len(instruc[0])-1])
			else:
				error_dupli.append(i)
		counter=counter+1

flag=False
for i in range(len(list_of_instructions)):
	instruc=list_of_instructions[i]
	if(instruc[0]=="var" and flag==False):
		var[instruc[1]]=counter
		counter=counter+1
	elif(instruc[0]=="var" and flag==True):
		error_var.append(i)
	else:
		flag=True


