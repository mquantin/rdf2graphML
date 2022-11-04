import re
import rdflib

def getValue(uri, predicateRegex):
    g = rdflib.Graph()
    returnValue = 'notFound'
    try:
        g.parse(uri)
        for s, p, o in g:
            if re.search(predicateRegex, p):
                #print(value,p, o)
                print('\nok ', uri,'\n\t', o.toPython())
                returnValue = o.toPython()#get only the first value
                break
        if returnValue == 'notFound':
            print('\nNOK ', uri)
    except:
        print(f"\nNOK {uri} {predicateRegex}")
        if re.search('/page/', uri):
            print('\t WARNING URI contains _page_ string, not rdf data, human readable version')
    return(returnValue)
