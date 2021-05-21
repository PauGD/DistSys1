                                                                                       
import xmlrpc.client
import time
import json 

class countWords():

    def contar():
        print(" prova correcta")


proxy = xmlrpc.client.ServerProxy('http://localhost:9000')


treball= { "ID": 00 , "Tipus": "word", "URL" : "http://127.0.0.1:5000/flaskFiles/fitxer1.txt" }
a= json.dumps(treball)

proxy.createWorker( )
proxy.createWorker()

#a= countWords()
proxy.addjob( a)





