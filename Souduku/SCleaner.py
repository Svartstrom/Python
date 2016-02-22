A = open('SolvedSoudukuBoard1.txt','r')
#B = open('SolvedSoudukuBoard1_Clean.txt','r+')

old = ""
for new in A:
	ok = 0
	if new == old:
		continue
	B = open('SolvedSoudukuBoard1_Clean.txt','r')
	for older in B:
		if older == new:
			print older
			break
		ok = 1
	if ok == 1:
		B.close()
		B=open('SolvedSoudukuBoard1_Clean.txt','a')
		B.write(new)
		old = new
	B.close()