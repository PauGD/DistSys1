import xmlrpc.client
import time
import json


proxy = xmlrpc.client.ServerProxy('http://localhost:9000')


treball = {"ID": 9 , "Tipus": "Count", "URL" : "http://127.0.0.1:5000/flaskFiles/fitxer1.txt"}
treball2 = {"ID": 30 , "Tipus": "Word", "URL" : "http://127.0.0.1:5000/flaskFiles/fitxer1.txt http://127.0.0.1:5000/flaskFiles/fitxer2.txt http://127.0.0.1:5000/flaskFiles/fitxer1.txt http://127.0.0.1:5000/flaskFiles/fitxer2.txt"}

a = json.dumps(treball)
b = json.dumps(treball2)
proxy.createWorker()
proxy.createWorker()
proxy.createWorker()


print(proxy.addJob(a))
print(proxy.addMultipleJobs(b))
