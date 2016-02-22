import re

Board = ([[0 for x in range(9)]for y in range(9)] for z in range(2))
Board = [0 for x in range(162)]

def checkFree(j,row,col=-1):
	if col==-1:
		col=row%9
		row=row/9
	found, Nfound = 0,1
	for poss in range(81):
		if poss % 9 == col or poss / 9 == row or ((poss/9)/3==row/3 and (poss%9)/3==col/3):
			if Board[poss] == j or Board[poss+81] == j:
				return found
	return Nfound

def printRoute(S):
	h = open("SolvedSoudukuBoard1.txt","a")
	for i in range(81,81*2):
		if S[i] is not 0:
			h.write(str(S[i]))
			#print S[i],
	h.write("\n")
	#print ""
def solveS(S,n):
	if n==81:
		return 0
	if S[n]==0:
		for i in range(10):
			#print i,
			if checkFree(i,n):
				S[n+81]=int(i)
				#print "Free"
				if solveS(S,n+1):
					return 1
				S[n+81]=int(0)
			else:
				printRoute(S)
	elif solveS(S,n+1):
		return 1
	return 0

H = open("p096_sudoku_first.txt","r")
for line in H:
	if line[0]=='':
		jj=0
	elif line[0]=='G':
		jj=0
		Name = line
	else:
		jj=0
		for ii in line:
			try:
				Board[jj]= int(ii)
			except: 
				pass
			jj+=1
print Name

#for l in range(1):
#	for r in range(9):
#		for c in range(9):
#			for j in range(1,10):
#				if checkFree(2,r,c):
#					Board[c+9*r+81*0]=0.1
solveS(Board,0)
print ""
for l in range(2):
	for r in range(9):
		for c in range(9):
			if not l:
				print "%.0f " % Board[c+9*r+81*l],
			else:
				print "%.0f " % int(int(Board[c+9*r])+int(Board[c+9*r+81*l])),
				#print "%.0f " % Board[c+9*r+81*l],#+Board[c+9*r+81*l],
		print ""
	print ""	