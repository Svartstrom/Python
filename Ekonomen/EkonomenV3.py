import re
import sys
def isLeapyear(n):
    if (n%400==0):
        return 1
    elif(n%100==0):
        return 0
    elif(n%4==0):
        return 1
    else:
        return 0
def findFile():
    saldoOverTime = []
    Yesterday = []
    if (len(sys.argv) > 1):
        return sys.argv[1]
    else:
        print 'Warning, no file given.'
        print 'You have to give a file as:'
        print "'python Ekonomen.py MyBankStatement.txt'"
        exit()

def processFile(fileToRead):
    print fileToRead
    year,month,date,text,saldo,i=0,0,0,'',0,0
    saldoOverTime=[]
    data = [year,month,date,text,saldo]
    with open(fileToRead,'r') as f:
        lines = f.readlines()
    for a in lines:
        Yesterday = [year, month, date, saldo]
        
        fullDate = re.search(r'^ *(\d\d\d\d)-(\d\d)-(\d\d)',a)
        medelande = re.search(r'\d *([A-Za-z0-9]*) *-|\d*',a)
        print medelande.group(1)
        year = abs(int(fullDate.group(1)))
        month = abs(int(fullDate.group(2)))
        date = abs(int(fullDate.group(3)))
        
        #a = re.sub(r',(P(k)[0-9]*) ',',(k):',a)
        saldo = re.search(r'([ \d*]*),\d\d$',a)
        
        saldo = re.sub(' ','',saldo.group(1))
        saldo = abs(int(saldo))
        
        done = 0
        
#Saving stuff
        if (saldoOverTime == []):
            print 'First date was:',str(year),str(month),str(date)
            saldoOverTime = [[year,month,date,saldo]]
        else:  #if (saldoOverTime == []):
            while(not done):
                if(year == Yesterday[0]):
                    #print 'the year is',str(year)
                    #print 'are you saying',str(month),'>',str(Yesterday[1])
                    if(month == Yesterday[1]):
                        #print 'the month is',str(month)
                        if(date == Yesterday[2]-1):         #Life is OK and we kan write 
                            saldoOverTime.append([year,month,date,saldo])
                            done = 1
                        elif( date < Yesterday[2]-1 ):      #OK day, but no transaction on that day
                            saldoOverTime.append([Yesterday[0],Yesterday[1],Yesterday[2]-1,Yesterday[3]])
                            Yesterday[2] -= 1               #We need to decrese the day with one
                        elif( date == Yesterday[2] ):
                            saldoOverTime.append([year,month,date,saldo])
                            done=1
                        elif( date > Yesterday[2] ):
                            print 'Frekking bank and not format its text!!!!!'
                            saldoOverTime.append([year,month,date,saldo])
                            done = 1
                    elif( month < Yesterday[1] ):
                        #print 'the month ougth to be',str(month)
                        if(Yesterday[2] == 1):              #If yesterday whas the first day of the prevous month
                            # we need to translate that date into the same day but the present month
                            if( Yesterday[1] == 1 or Yesterday[1] == 2 or Yesterday[1] == 4 or Yesterday[1] == 6 or Yesterday[1] == 8 or Yesterday[1] == 9 or  Yesterday[1] == 11):
                                Yesterday[2] = 32       # One after current month maximum
                                Yesterday[1] -= 1       # Decrese month by one to make it current month
                            elif( Yesterday[1] ==  5 or Yesterday[1] == 7 or Yesterday[1] == 10 or Yesterday[1] == 12):
                                Yesterday[2] = 31       # One after current month maximum
                                Yesterday[1] -= 1
                            elif( Yesterday[1] == 3):   # If it's a leap year, february is special...
                                if (isLeapyear(year)):
                                    Yesterday[2] = 30   # One after current month maximum
                                    Yesterday[1] -= 1
                                else:
                                    Yesterday[2] = 29   # One after current month maximum
                                    Yesterday[1] -= 1
                            if ( date == Yesterday[2]-1 ):      
                                saldoOverTime.append([year,month,date,saldo])
                                done = 1
                            elif( date < Yesterday[2]-1 ):      #OK day, but no transaction on that day
                                saldoOverTime.append([Yesterday[0],Yesterday[1],Yesterday[2]-1,Yesterday[3]])
                                Yesterday[2] -=1
                            elif( date > Yesterday[2] ):
                                print 'GOD darnit'
                                saldoOverTime.append([year,month,date,saldo])
                                done = 1
                        else:                          # if Yesterday was not the first of the month
                            saldoOverTime.append([Yesterday[0],Yesterday[1],Yesterday[2]-1,Yesterday[3]])
                            Yesterday[2]-=1
                    elif( month > Yesterday[1] ):
                        print 'FFS'
                        saldoOverTime.append([year,month,date,saldo])
                        done =1
                elif( year < Yesterday[0] ):############################################################################
                    if(Yesterday[2] == 1):              #If yesterday whas the first day of the prevous month
                        print 'Entering',str(year)
                        Yesterday[2] = 32       # One after current month maximum
                        Yesterday[1] = 12
                        Yesterday[0] -= 1       # Decrese year by one to make it current year
                        if ( date == Yesterday[2]-1 ):      
                            saldoOverTime.append([year,month,date,saldo])
                            done = 1
                        elif( date < Yesterday[2]-1 ):      #OK day, but no transaction on that day
                            saldoOverTime.append([Yesterday[0],Yesterday[1],Yesterday[2]-1,Yesterday[3]])
                            Yesterday[2] -=1
                    else:                          # if Yesterday was not the first of the month
                        saldoOverTime.append([Yesterday[0],Yesterday[1],Yesterday[2]-1,Yesterday[3]])
                        Yesterday[2]-=1
        data.append([year,month,date,text,saldo])
    return data
#print 'Last date was:',str(year),str(month),str(date)
#with open('saldo.txt','w') as m:        
#    for a in range(len(saldoOverTime)):
#        toWrite = str(saldoOverTime[a][0])+'-'+str(saldoOverTime[a][1])+'-'+str(saldoOverTime[a][2])+' '+str(saldoOverTime[a][3])+'\n'
#        m.write(toWrite)

i=0
fileToRead = findFile()
hej = processFile(fileToRead)
fileToWriteTo = sys.argv[1]+'.m'
#with open(fileToWriteTo,'w') as m:
#    m.write('clear all, close all, clc,hold on\n')
#    m.write('plot([ ...\n')
#    for a in range(len(saldoOverTime)):
#        #toWriteMatlab = "plot('+str(-i)+','+str(saldoOverTime[a][3])+",'*');\n"
#        toWriteMatlab = str(saldoOverTime[-a][3])+' ...\n'
#        m.write(toWriteMatlab)
#        i+=1
#    m.write('])')
    
print fileToWriteTo
print hej
