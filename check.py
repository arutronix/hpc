import os
import os.path
from os import makedirs
import shutil

from mpi4py import MPI
import time

comm = MPI.COMM_WORLD
path = os.getcwd() 

source = 'kaps.glm'
allDataset = "all_data_set"
loaddata = "load_data"
homenodes = "number_of_homes_nodes"

#i is for penetration level

for i in range(1,10):
	execPlayerStart = time.time()
	newDir = "PV_"+str(i*10)+"_"+str(comm.rank)+"_proc_"+str(comm.rank)

	dir_Name = newDir+"/csv_output"
	os.makedirs(dir_Name)
	shutil.copy(source, newDir)
	
	playerpy = "player_file_generation_"+str(i*10)+".py"
	shutil.copy("player_file_generation_"+str(i*10)+".py", newDir)
			
	dir_Name = newDir+'/Player_File'
	os.makedirs(dir_Name)	
				
	shutil.copytree(allDataset, newDir+"/all_data_set")
			
	shutil.copytree(loaddata, newDir+"/load_data")	
	
	shutil.copytree(homenodes, newDir+"/number_of_homes_nodes")	

	os.chdir(newDir)

	os.system("python %s"%playerpy)
	
	execPlayerEnd = time.time();
	execPlayerTime = execPlayerEnd - execPlayerStart;
	print("Generation of Player file time is: %d" % (execPlayerTime))
	
	execStart = time.time()
	
	os.system("gridlabd %s"%source)
	
	execEnd = time.time();
	execTime = execEnd - execStart;
	print("Execution time of gridlabd is: %d" % (execTime))
	
	#comm.Barrier()

	shutil.rmtree(allDataset)
	shutil.rmtree(loaddata)
	shutil.rmtree(homenodes)
	shutil.rmtree("Player_File")
	os.remove("kaps.glm")
	os.remove("player_file_generation_"+str(i*10)+".py")
	#os.remove("R1-12.47-1_capacitor1.csv")
	#os.remove("R1-12.47-2_capacitor2.csv")
	#os.remove("R1-12.47-3_capacitor3.csv")
	#os.remove("R1-12.47-1_reg1_output.csv")
	
	os.chdir("..")
	


#print("Hello! I'm rank %d from %d running in total..." % (comm.rank, comm.size))


comm.Barrier()