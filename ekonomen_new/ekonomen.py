# coding=utf-8

#import dataReader.py

from collections import deque
import threading
import time
import glob

global que1, que2, que3
que1 = deque([['WAIT']])
que2 = deque([[]])
que3 = deque([[]])

global killSignal
killSignal = "N"

# readFromXLSX(db,ORGname,ij,max_ant):

def reader():
    global que1, qu2, que3, killSignal
    while True:
        if ( len(que1) > 0 ):
            task = que1.popleft()
        else:
            if ( len(que2) > 0 ):
                task = que2.popleft()
            else:
                if ( len(que3) > 0 ):
                    task = que3.popleft()
                else:
                    task = ["WAIT"]
        if ( task == ["WAIT"] ):
            time.sleep(0.01)
        if ( task == ["PRINT_ALL"] ):
            for file in glob.glob("*"):
                print(file)
        if killSignal == "K":
            break
    print("Bye Bye reader")
    

def GUI():
    global que1, qu2, que3, killSignal
    while True:
        options = ["Wait (w):",
                   "Print all (p):",
                   #"Quit:",
                   "Quit (q):"]
        print("que1: "+str(len(que1)))
        print("que2: "+str(len(que2)))
        print("que3: "+str(len(que3)))
        for i,c in enumerate(options):
            if c == "Quit (q):":
                quitID = str(i)
            print(str(i)+": "+str(c))

        inp = input("Input: ")
        inp = str(inp)
            
        if inp == "q" or inp == quitID:
            killSignal = "K"
            break
        elif inp == "p":
            que2.append(["PRINT_ALL"])

    print("Bye Bye gui")
        
def main():
    global que1, qu2, que3, killSignal
    try:
        thread1 = threading.Thread(target=reader, args=())#masterThread( 1, "Reader" )
        thread2 = threading.Thread(target=GUI, args=())#masterThread( 2, "GUI" )
        #thread3 = masterThread( 3, "webServer" )
    except:
        print("Unable to start threads!")

    thread1.start()
    thread2.start()
    #thread3.start()
    while True:
        if killSignal == "K":
            break
    print("Bye Bye main")

if __name__ == "__main__":
    main()
