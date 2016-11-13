import re
import sys
import glob


class month:
    def __init__(self):
        self.totIn=0
        self.totOut=0
        self.Messages=[]
    def add(self,value,text):
        if text not in self.Messages:
            self.Messages.append(text)
            if int(value) > 0:
                self.totIn += int(value)
            else:
                self.totOut -= int(value)
    def printme(self,msg):
        print "Total income: "+str(self.totIn)+"   Total expences: "+str(self.totOut)
        if msg:
            print self.Messages
    def saldo(self,Dir):
        if Dir == 'In':
            return self.totIn
        elif Dir == 'Out':
            return self.totOut
    #__init__(self)

class year:
    def __init__(self):
        self.totIn=0
        self.totOut=0
        self.months = {}

    def add(self,Imonth,value,text):
        if Imonth not in self.months:
            self.months[Imonth]=month()
            self.months[Imonth].add(value,text)
        else:
            self.months[Imonth].add(value,text)

    def updateSaldo(self):
        self.totIn = self.totOut = 0
        for Inst in self.months:
            #self.months[Inst].updateSaldo()
            self.totIn += self.months[Inst].saldo("In")
            self.totOut += self.months[Inst].saldo('Out')

    def printme(self,msg):
        print "Total yearly income: "+str(self.totIn)+"   Total yearly expences: "+str(self.totOut)
        print "Saldo: "+str(self.totIn - self.totOut)
        for Inst in self.months:
            pass

    def saldo(self,Dir):
        if Dir == 'In':
            return self.totIn
        elif Dir == 'Out':
            return self.totOut            

            #print "The month is: "+str(Inst)
            #self.months[Inst].printme(msg)
class master:
    def __init__(self):
        self.totIn=0
        self.totOut=0
        self.years = {}
    def add(self,Iyear,month,value,text):
        if Iyear not in self.years:
            self.years[Iyear]=year()
            self.years[Iyear].add(month,value,text)
        else:
            self.years[Iyear].add(month,value,text)

    def updateSaldo(self):
        self.totIn = self.totOut = 0
        for Inst in self.years:
            self.years[Inst].updateSaldo()
            self.totIn += self.years[Inst].saldo("In")
            self.totOut += self.years[Inst].saldo('Out')

    def printme(self,msg):
        print "Total income: "+str(self.totIn)+"   Total expences: "+str(self.totOut)
        print "Saldo: "+str(self.totIn - self.totOut)
        for Inst in self.years:
            print ""
            print "The year is: "+str(Inst)
            self.years[Inst].printme(msg)

class menuTop:
    def __init__(self):
        self.name = "Main menu"
        self.child
    def printChild(self):
        for a in self.child:
            print a.name
    def gotoChild(self,n):
        pass

class mainMenu:
    def __self__(self):
        self.name = "Main menu"
        self.Stack
    def printStack(self):
        ii = 1
        for item in self.Stack:
            print str(ii)+": "+item.name
            ii += 1

#    def Pop(self):
#        if self.Stack[-1] is not []:
#            ret = self.Stack[-1]
#            self.Stack = self.Stack[:-1]
#    def Put(self,n):
#        self.Stack.append(n)

def findFile():
    files = []    
    if (len(sys.argv) > 1):
        return sys.argv[1]
    else:
        print 'Warning, no file given.'
        print 'You have to give a file as:'
        print "'python Ekonomen.py MyBankStatement.txt'"
        exit()


def processFile(fileToRead,master):
    #print fileToRead
    year,month,date,text,saldo,i=0,0,0,'',0,0
    saldoOverTime=[]
    data = [year,month,date,text,saldo]
    with open(fileToRead,'r') as f:
        lines = f.readlines()
    for a in lines:
        Yesterday = [year, month, date, saldo]
        
        fullDate = re.search(r'^ *(\d\d\d\d)-(\d\d)-(\d\d)',a)
        
        meddelande = re.search(r'([0-9]{5,})',a)
        meddelande1 = re.search(r'-\d\d ?\t ?([^\t]*)\t',a) 
        print meddelande1.group(1)
        year = abs(int(fullDate.group(1)))
        month = abs(int(fullDate.group(2)))
        date = abs(int(fullDate.group(3)))
        
        #a = re.sub(r',(P(k)[0-9]*) ',',(k):',a)
#       2012-11-25 	FRAN SHB 	00000000000000000 	20 000,00 	91 688,97
        saldo = re.search(r'\t([ \d*]*,\d\d)$',a)
        transfer = re.search(r'\t ?([-]?[ \d*]*),\d\d ?\t',a)
        
        saldo = re.sub(' ','',saldo.group(1))
        transfer = re.sub(' ','',transfer.group(1))
        saldo = re.sub(',','.',saldo)
        
        text = str(year)+str(month)+str(date)+str(transfer)+str(meddelande.group(1))
#saldo = abs(int(saldo))
        #print year, month, date,text, transfer,saldo
        Eko.add(year,month,transfer,text)
        Eko.updateSaldo()
#        add(self,year,month,value,text):

def GInp():
    try:
        UI = raw_input() # raw_input in Python 2.x
        if not UI:
            UI=0
            #raise ValueError('empty string')
    except ValueError as e:
        print(e)
    return UI

def menu(Eko,Jek):
    user_input = -1
    menuText = {
        '1':"1. View existing files.\n2. Print current file.\n0. Exit."
        }
    MainMenu="What would you like to do?\n1. Load file.\n2. Print current file.\n0. Exit."
    LoadMenu="\nPress the number coresponding to your desired file, or start typing the name of the file you whant to read."
    print "Hello!"
    while user_input != 0:
       print MainMenu 
       try:
           user_input = int(GInp())
       except:
           print "Input have to be a numeral\n"
           user_input = -1
       
       if user_input == 1:
           print LoadMenu
           Int = 1
           print "0. Back."
           for Inst in Jek:
               print str(Int)+". "+Inst
               Int+=1
           user_input_load = GInp()
           try:
               user_input_load=int(user_input_load)-1
           except:
               if user_input_load not in All:
                   print user_input_load+" is not a existing file."
           print Jek[0]
           processFile(Jek[user_input_load],master)
       if user_input == 2:
           print Eko.printme("Hello!")

MainMenu = mainMenu()



#fileToRead = findFile()
Eko=master()
Jek1 = glob.glob("*.Jek")
Jek2 = glob.glob("*.txt")
Jek=Jek1+Jek2
#hej = processFile(fileToRead,Eko)
#Eko.printme(0)
menu(Eko, Jek)
