
from multiprocessing import Process
from xmlrpc.server import SimpleXMLRPCServer
import os
import logging
import time
PROCES_PID=0
PROCES_LIST= {} # set=  PID:proc

logging.basicConfig(level=logging.INFO)

server = SimpleXMLRPCServer(
    ('localhost', 9000),
    logRequests=True,
)

def startWorker( PROCES_PID):
   while (1):
        print('aiaiai') 



def createWorker():
    global PROCES_PID
    global PROCES_LIST

    proc=Process(target= startWorker, args=(PROCES_PID,))
    proc.start()


    proc.join

    PROCES_LIST[PROCES_PID]=proc
    PROCES_PID += 1


def deleteWorker( PID):
    global PROCES_LIST

    procac= PROCES_LIST[PID]

    procac.kill()

def list_contents(dir_name):
    logging.info('list_contents(%s)', dir_name)
    return os.listdir(dir_name)

server.register_function(list_contents)
server.register_function(deleteWorker)
server.register_function(createWorker)
server.register_function(startWorker)

#def listWorkers():

try:
    print('Use Control-C to exit')
    server.serve_forever()
except KeyboardInterrupt:
    print('Exiting')

