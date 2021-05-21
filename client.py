                                                                                       
import xmlrpc.client
import time
import json 




proxy = xmlrpc.client.ServerProxy('http://localhost:9000')


treball= { "ID": 00 , "Tipus": "word", "URL" : "http://127.0.0.1:5000/flaskFiles/fitxer1.txt" }
treball2= { "ID": 00 , "Tipus": "Count", "URL" : "http://127.0.0.1:5000/flaskFiles/fitxer1.txt http://127.0.0.1:5000/flaskFiles/fitxer2.txt" }

a= json.dumps(treball)
b= json.dumps(treball2)
proxy.createWorker( )
proxy.createWorker()

#a= countWords()
proxy.addjob( a)
proxy.addMultipleJobs(b)




