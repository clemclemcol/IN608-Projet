import os
import re #regex 
	
def create_fil(tot_MSD):
	print("creation\n")
	
	num = 0
	den = 0 
	avg = 0 
		
	file = open("Results_total_PG.txt", "a")
	for y in range(2):
		if (y == 0) : 
			k = 5
		if (y == 1) :
			k = 10
		for z in range(6):
			if (z == 0) : 
				nbpoints = 50
			if (z == 1) :
				nbpoints = 100
			if (z == 2) : 
				nbpoints = 500
			if (z == 3) :
				nbpoints = 1000
			if (z == 4) : 
				nbpoints = 5000
			if (z == 5) :
				nbpoints = 10000
			
			print("K = " + str(k) + "\t" + "nb points : " + str(nbpoints) )
			file.write("K = " + str(k) + "\t" + "nb points : " + str(nbpoints) + "\n")
			
			if (tot_MSD[z][y]["min"] == 99):
		
				print("min MSD \t " + str(0) )
				file.write("min MSD \t " + str(0) + "\n")
			else : 
				print("min MSD \t " + str(tot_MSD[z][y]["min"]) )
				file.write("min MSD \t " + str(tot_MSD[z][y]["min"]) + "\n")
			
			for i in range(len(tot_MSD[z][y]["avg"])):
				num = num + (float(tot_MSD[z][y]["avg"][i])*float(tot_MSD[z][y]["tests"][i]))
				den = den + float(tot_MSD[z][y]["tests"][i])
			if (den):
				avg = round(num/den, 3)
			
			print("avg MSD \t " + str(avg) )
			file.write("avg MSD \t " + str(avg) + "\n")
			
			print("max MSD \t " + str(tot_MSD[z][y]["max"]) )
			file.write("max MSD \t " + str(tot_MSD[z][y]["max"]) + "\n")
			
			print("__" )
			file.write("__" + "\n")
			num = 0
			den = 0 
			avg = 0 
		
    
	file.close()

def lecture_file(name_files, tot_MSD):
		
	nb_clusters = ["5", "10"]
	nb_points = ["50","100","500","1000","5000","10000"]
	
	i = 0
	j = 0
	
	file = open(name_files, "r")
	print("ouverture")
	line = file.readline()
	m = re.match(r'Nombre tests = (\d+)', line) 
	nbtestsF = int(m.group(1))
	line = file.readline()	
	#print(line)
	
	while line : 
		n = re.match(r'Nombre tests = (\d+)', line)
		if n : 
			line = file.readline()
		
		m = re.match(r'K = (\d+)	nb points : (\d+)', line) 			#recupere les valeurs de K et du nombre de points dans fichier /!\ espacement important
		if m :
			print(str(m.group(1)))
			print(str(m.group(2)))	
		else :
			#print(line)
			print("no match.")
			exit(1)
			
		if (str(m.group(1)) in nb_clusters):							#["5", "10"]
			i = nb_clusters.index(str(m.group(1)))
			print("i: ", i )
			
		if (str(m.group(2)) in nb_points):								#["50","100","500","1000","5000","10000"]
			j = nb_points.index(str(m.group(2)))
			print("j: ", j )
		#print ('old: ', tot_MSD[j][i])
		
		tot_MSD[j][i]["tests"].append(int(nbtestsF))
		for x in range(0, 3):	
			line = file.readline()
			#print(line)
			match = re.match(r'(\w+) MSD 	 (\d+.\d+)', line) 			#min MSD 	 2.92 /!\ espacement important
			#print(str(match.group(1)))
					
			type = str(match.group(1))
			val = float(match.group(2))
			#print("val: " + str(match.group(2)))	
			if (type == "min"):
				if (val < tot_MSD[j][i]["min"]):
					tot_MSD[j][i].update({"min": val})
					#print("changement min")
					
			elif (type == "avg"):
				tot_MSD[j][i]["avg"].append(val)
				
			elif (type == "max"):
				if (val > tot_MSD[j][i]["max"]):
					tot_MSD[j][i].update({"max": val})
					#print ("changement max")	
							
		print ("new : ", tot_MSD[j][i])									
		file.readline()
		line = file.readline()
		print(line)
								
	file.close()
	#print (tot_MSD)
	return tot_MSD

def parallelisation(path_dir):

	if (path_dir ==0): 
		print("Erreur path.")
	
	tot_MSD = []
	for r in range (6):
		tot_MSD.append([{"min": 99, "avg": [], "max": 0, "tests":[]},{"min": 99, "avg": [], "max": 0, "tests":[]}])

	for name_file in os.listdir(path_dir):
		print(name_file)
		m = re.match(r"resultat_PG\w+.txt", name_file) 
		
		print (m)
		if (m):
			print('-> lecture')
			lecture_file(name_file, tot_MSD)
			#print (tot_MSD)
		
	create_fil(tot_MSD)
	print("c'est fait")
		
	

