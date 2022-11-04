import re
import rdflib

def getValue(uri, predicateRegex):
    g = rdflib.Graph()
    try:
        g.parse(uri)
        for s, p, o in g:
            if re.search(predicateRegex, p):
                #print(value,p, o)
                print('fetched data from ', uri)
                return o.toPython()#get only the first value
    except:
        print(f"nothing for {predicateRegex} \n\t in {uri}")
        if re.search('/page/', uri):
            print('\t WARNING URI contains _page_ string, \n\t not rdf data, human readable version')
        else:
            print('\t check URI')
        return('notFound')
