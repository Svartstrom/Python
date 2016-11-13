import re
import sys

if (len(sys.argv) > 1):
    fileToRead = sys.argv[1]
else:
    print 'Warning, no file given.'
    print 'You have to give a file as:'
    print "'python EkonomenHomo.py MyBankStatement.txt'"
    exit()

with open(fileToRead,'r') as f:
    lines = f.readlines()
for a in lines:
    saldo = re.sub(',\d\d','',a)#saldo.group(0))
    
    print saldo#done = 0
