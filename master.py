from multiprocessing import Process
from xmlrpc.server import SimpleXMLRPCServer
import os
import logging
import time
import redis
from flask import Flask
from prova import app
import requests
import copy
import json
#app.run()


re= redis.Redis(host = 'localhost', port = 6379, db = 0)

PROCES_PID = 0
PROCES_LIST = {} # set=  PID:proc


logging.basicConfig(level = logging.INFO)

server = SimpleXMLRPCServer(
    ('localhost', 9000),
    logRequests = True,
)

def startWorker( PROCES_PID):
    re = redis.Redis(host = 'localhost', port = 6379, db = 0)
    result = ""
    while (1):
        a = re.rpop("JobList")
        if a != None:
            #print(a)
            data = json.loads(a)
            url = data['URL']
            fitxer = requests.get(url)
            if(fitxer.status_code == 500):
                print("ERROR FILE NOT FOUND")
                exit(0)
            else:
                if(data['Tipus'] == "Count"):
            	    result0 = countWords(fitxer.text)
                    result = str(result0)
                else:
                    if(data['Tipus'] == "Word"):
                        result = wordCount(fitxer.text)

            re.lpush(data['ID'], result)

            time.sleep(5)

#def addResults():sortida ="El resultat es:"for keys, value in tupla.items():sortida += str(keys)sortida += str("->")sortida += str(value)sortida += str("---- ")print(sortida)

def countWords(filetext):
    word = filetext.split()
    return(len(word))

def wordCount(filetext):
    separated = filetext.split()
    llistaoccur = []
    tuplenames = {}
    for i in separated:
        if i not in llistaoccur:
            llistaoccur.append(i)

    for j in range(0, len(llistaoccur)):
        tuplenames[llistaoccur[j]] = separated.count(llistaoccur[j])

    return tuplenames


def addJob(argument):
    re.lpush("JobList", argument)
    data = json.loads(argument)
    mult = re.lpop(data['ID'])
    #print(mult)
    return 0


def addMultipleJobs(argument):
    data = json.loads(argument)
    url = data['URL']
    multipleurl = url.split()
    for i in range(0, len(multipleurl)):
        data['URL'] = multipleurl[i]
        abc = json.dumps(data)
        re.lpush("JobList", abc)

    return 0


def createWorker():
    global PROCES_PID
    global PROCES_LIST

    proc = Process(target = startWorker, args = (PROCES_PID,))
    proc.start()

    PROCES_LIST[PROCES_PID] = proc
    PROCES_PID += 1

    return 0


def deleteWorker(PID):
    global PROCES_LIST

    procac = PROCES_LIST[PID]

    procac.kill()

def list_contents(dir_name):
    logging.info('list_contents(%s)', dir_name)
    return os.listdir(dir_name)

server.register_function(list_contents)
server.register_function(deleteWorker)
server.register_function(createWorker)
server.register_function(startWorker)
server.register_function(addJob)
server.register_function(addMultipleJobs)


try:
    print('Use Control-C to exit')
    server.serve_forever()
except KeyboardInterrupt:
    print('Exiting')
