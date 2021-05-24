from fireREST import FMC
import json

fmc = FMC(hostname='220.181.130.66:18443', username='admin', password='P@sw0rd@!@#$%', domain='Global')
#fmc = FMC(hostname='fmcrestapisandbox.cisco.com/api/api-explorer/', username='admin', password='1vtG@lw@y')
output = fmc.object.interface.get()

print(type(output))
