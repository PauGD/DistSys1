                                                                                       
import xmlrpc.client
import time

class countWords():

    def contar():
        print(" prova correcta")


proxy = xmlrpc.client.ServerProxy('http://localhost:9000')



proxy.createWorker( )
proxy.createWorker()

#a= countWords()
proxy.addjob( "a" )





