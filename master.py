
from multiprocessing import Process
from xmlrpc.server import SimpleXMLRPCServer
import os
import logging
import time
import redis
from flask import Flask
from prova import app


#app.run()


re= redis.Redis( host= 'localhost', port=6379,db=0)

PROCES_PID=0
PROCES_LIST= {} # set=  PID:proc


logging.basicConfig(level=logging.INFO)

server = SimpleXMLRPCServer(
    ('localhost', 9000),
    logRequests=True,
)

def startWorker( PROCES_PID):
    re= redis.Redis(host= 'localhost', port=6379,db=0)
    while (1):
        a=re.rpop("JobList")
        if a!= None:
            print(a)
            time.sleep(5)


def addjob( argument ):

    re.lpush( "JobList", argument)

    return 0
    


def createWorker():
    global PROCES_PID
    global PROCES_LIST

    proc=Process(target= startWorker, args=(PROCES_PID,))
    proc.start()


    PROCES_LIST[PROCES_PID]=proc
    PROCES_PID += 1

    return 0


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
server.register_function(addjob)
#def listWorkers():

try:
    print('Use Control-C to exit')
    server.serve_forever()  
except KeyboardInterrupt:
    print('Exiting')

