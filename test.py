import json
from multiprocessing.pool import ThreadPool

import dns.message
import dns.query


class dnsTester:
    def __init__(self):
        self.unfiltered_resolvers={
        "cloudflare":"1.1.1.1",
        "google":"8.8.8.8"
        }
        self.filtered_resolvers={
        "cloudflare_family":"1.1.1.2",
        "quad9":"9.9.9.9",
        "dns.EU":"193.110.81.0",
        "dns.EU.Zero":"193.110.81.9",
        "cleanBrowsing":"185.228.168.9",
        "openDNS":"208.67.222.123"
        }

    def __resolve(self,domain,dnsServer):
        dnsQuery=dns.message.make_query(domain,'A')
        response=dns.query.udp(dnsQuery,dnsServer)
        return response

    def testDomain(self,domain):
        domainResult=[]
        domainValid=False
        for name,server in self.unfiltered_resolvers.items():
            domainValid=domainValid or (len(self.__resolve(domain,server).answer)>0)
        if domainValid:
            for name,server in self.filtered_resolvers.items():
                blocked=(len(self.__resolve(domain,server).answer)==0)
                domainResult.append({name:blocked})
        return {domain:domainResult}

pool = ThreadPool(processes=8)

with open('domains.txt') as d:
    domains=d.read().splitlines()

results=[]
myDnsTester=dnsTester()

res = pool.map(myDnsTester.testDomain,domains)


with open('output.json','w+') as j:
    json.dump(res,j)


