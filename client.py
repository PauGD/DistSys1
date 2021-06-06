import xmlrpc.client
import time
import json
import click
import random

IDP=0
proxy = xmlrpc.client.ServerProxy('http://localhost:9000')



@click.group( invoke_without_command=False)
@click.pass_context
def cli(ctx):
    pass

@cli.command('addJob')
@click.argument('url')
@click.option('--type','-a')
def main(url,type):
    id=random.randint(0,500)
    click.echo(type)
    treball = {"ID": id , "Tipus": type , "URL" : url}
    a=json.dumps(treball)
    print(proxy.addJob(a))

@cli.command('addWorker')
def addWorker():
    proxy.createWorker()



@cli.command('listWorkers')
def listWorkers():
    print(proxy.listWorkers())

@cli.command('deleteWorker')
@click.argument('nwor', type= int)
def delete(nwor):
    print(nwor)
    a=proxy.deleteWorker(nwor)
    if(a==0):
        print("No hi ha cap treballador amb aquesta ID")

@cli.command('addMultipleJobs')
@click.argument('url', nargs=-1)
@click.option('--type','-a')
def main(url,type):
    id= random.randint(0,500)
    str=""
    for i in url:
        str+=i
        str+=" "

    print(str)
    treball = {"ID": id , "Tipus": type , "URL" : str}
    a=json.dumps(treball)
    print(proxy.addMultipleJobs(a))


if __name__ == '__main__':
    cli()
