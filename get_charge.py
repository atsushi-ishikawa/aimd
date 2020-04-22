import subprocess
import os, sys
#
# get number of atoms from file
#
argvs = sys.argv
charge_file = argvs[1]
chargefile = "charges.dat"
spinfile = "spins.dat"

fc = open(chargefile,"w")
fs = open(spinfile,"w")

has_spin = True # whether UKS or not
takesum  = False # whether to take partial charge sum or not

line = subprocess.Popen('grep "Total" %s --line-number | head -1' % charge_file, stdout=subprocess.PIPE, shell=True).communicate()[0]
natom = int(line.split(":")[0]) - 6

charge = [ [] for i in range(natom+1) ]
if has_spin:
	spin = [ [] for i in range(natom+1) ]

with open(charge_file, "r") as f:
	for line in f:
		try:
			num = int(line.split()[0])
		except:
			pass
		else:
			if has_spin:
				chg = float(line.split()[5])
				spn = float(line.split()[6])
				charge[num].append(chg)
				spin[num].append(spn)
			else:
				chg = float(line.split()[4])
				charge[num].append(chg)

nstep = len(charge[1])

# take summation by part
if takesum:
	sumlist = [81,82,84,85] # step
	#sumlist = [65,67,68,69]  # li-doped

	for istep in range(nstep):
		if has_spin:
			sum1 = 0 ; sum2 = 0
			for i in sumlist:
				sum1 += charge[i][istep]
				sum2 += spin[i][istep]
			print sum1, sum2
		else:
			sum1 = 0
			for i in sumlist:
				sum1 += charge[i][istep]

			print sum1
else:
	for istep in range(nstep):
		for iatom in range(1,natom+1):
			#sys.stdout.write("%8.4f" % charge[iatom][istep])
			#sys.stdout.write("%8.4f" % spin[iatom][istep])
			fc.write("%8.4f" % charge[iatom][istep])
			if has_spin:
				fs.write("%8.4f" % spin[iatom][istep])

		#sys.stdout.write("\n")
		fc.write("\n")
		fs.write("\n")

