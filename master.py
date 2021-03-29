
from multiprocessing import Process
import time
PROCES_PID=0
PROCES_LIST= {} # set=  PID:proc

def start_worker( PROCES_PID):
   while (1):
        print( 'aiaiai') 



def createWorker():
    global PROCES_PID
    global PROCES_LIST

    proc=Process( target= start_worker ,args=( PROCES_PID ,))
    proc.start()


    proc.join

    PROCES_LIST[PROCES_PID]=proc
    PROCES_PID += 1


def deleteWorker( PID):
    global PROCES_LIST

    procac= PROCES_LIST[PID]

    procac.kill()



#def listWorkers():



createWorker()
print( 'aiaiai')
time.sleep(2)
deleteWorker(0)
