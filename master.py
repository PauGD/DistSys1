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


re = redis.Redis(host = 'localhost', port = 6379, db = 0)


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
        element = re.brpop("JobList")[1]
        if element != None:
            data = json.loads(element)
            if(data['Tipus'] != "Add"):
                url = data['URL']
                fitxer = requests.get(url)
                if(fitxer.status_code == 500):
                    print("ERROR FILE NOT FOUND")
                    exit(0)
                else:
                    if(data['Tipus'] == "Count"):
                        result0 = countWords(fitxer.text)
                        result = json.dumps(result0)
                    else:
                        if(data['Tipus'] == "Word"):
                            result0 = wordCount(fitxer.text)
                            result = json.dumps(result0)
                    requests.delete(url)
                    re.lpush(data['ID'], result)
            else:
                if(data['Tipus'] == "Add"):
                    element1 = addResults(re, element)

            time.sleep(1)

#def addResults(): sortida ="El resultat es:"for keys, value in tupla.items():sortida += str(keys)sortida += str("->") sortida += str(value) sortida += str("---- ")print(sortida)

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
    mult = re.brpop(data['ID'])[1]
    return mult


def addMultipleJobs(argument):
    nElements = 0
    data = json.loads(argument)
    url = data['URL']
    multipleurl = url.split()
    for i in range(0, len(multipleurl)):
        data['URL'] = multipleurl[i]
        abc = json.dumps(data)
        re.lpush("JobList", abc)
        nElements = nElements + 1

    addWorker = {"ID": data['ID'], "Tipus": "Add", "URL" : nElements}
    addWorker2 = json.dumps(addWorker)
    re.lpush("JobList", addWorker2)

    data1 = "mult, result" + str(data['ID'])
    mult = re.brpop(data1)[1]

    return (mult)

def addResults(re, argument):
    data = json.loads(argument)
    url = data['URL']
    id = data['ID']
    element0 = re.blpop(id)[1]
    element0 = json.loads(element0)
    url = url - 1

    if type(element0) is dict:
        for i in range (url):
            element1 = re.blpop(id)[1]
            element1 = json.loads(element1)
            for key in element1:
                if(key in element0):
                    newElement = element1[key] + element0[key]
                else:
                    newElement = element1[key]
                element0[key] = newElement
    else:
        for i in range (url):
            element1 = re.blpop(id)[1]
            element1 = json.loads(element1)
            element0 = element0 + element1

    data1 = "mult, result" + str(data['ID'])
    mult = json.dumps(element0)
    re.lpush(data1, mult)

    return(0)

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
