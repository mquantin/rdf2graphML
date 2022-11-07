import re
import rdflib

def filterLang(prefLabels, langPattern, affiche):
    for label in prefLabels:
        if label.language and label.language.startswith(langPattern):
            if affiche:
                print(f'\t trouvé: {label.toPython()} ({label.language})')
            return label.toPython()


def getValue(uri, predicateRegex):
    g = rdflib.Graph()
    prefLabels = set()#maybe various values for one prop
    try:
        g.parse(uri)
        for s, p, o in g:
            if re.search(predicateRegex, p):
                prefLabels.add(o)
    except:
        print(f"NOK {uri}")
        if re.search('/page/', uri):
            print('\t URI contains _page_ string, not rdf data, human readable version')
        else:
            print('\t no triples at this URI, check spelling')
        return "notFound"
    if not prefLabels:
        print(f"NOK {uri}")
        print('\t predicate not found on URI')
        return "notFound"
    for langPattern in ['fr', 'en', 'it']:#lang choices by order of pref
        if filterLang(prefLabels, langPattern, False):
            print(f"OK {uri}")
            return filterLang(prefLabels, langPattern, True)
    #if none of the langPattern is found then
    default = prefLabels.pop()#else return any value
    print(f"OK {uri}")
    print(f'\t trouvé: {default.toPython()} ({default.language})')
    return default.toPython()
