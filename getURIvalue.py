import re
import rdflib
from rich import print
import yaml
from typing import NamedTuple


class PropVal(NamedTuple):
    """a tuple containing a property and its value"""
    prop: str
    val: str#set()#maybe various values for one prop



OK = "[green]OK[/green]"
NOK = "[bold red]NOK[/bold red]"
newKnownURIs = {}
KnownURIs_yamlFilepath = "knownURI.yml"#history of mapping URI->label to limit the number of http requests 




with open(KnownURIs_yamlFilepath) as KnownURIsFile:
    knownURIs = yaml.load(KnownURIsFile, Loader=yaml.CLoader)# dict with {URI:label} as {key:value}
    # for key, value in yaml_content.items():
    #     print(f"URI {key}: label {value}")



def filterPref(trouves):
    for langPattern in ['fr', 'en', 'it']:#lang choices by order of pref
        for trouve in trouves:
            if isinstance(trouve.val, rdflib.term.Literal) :
                if trouve.val.language and trouve.val.language.startswith(langPattern):
                    print(f'\t {OK} {trouve.prop}: {trouve.val} ({trouve.val.language})')
                    return trouve



def createNewURIrecord(uri, trouve):
    newURIrecord = {trouve.prop.toPython(): trouve.val.toPython()}
    if uri in newKnownURIs:
        newKnownURIs[uri].update(newURIrecord) 
    else: 
        newKnownURIs[uri] = newURIrecord



def getValue(uri, predicateRegexList):
    #lookup local known values. Avoid useless http requests
    if uri in knownURIs:
        for key, value in knownURIs[uri].items():
            for predicateRegex in predicateRegexList:
                if re.search(predicateRegex, key):
                    print(f'\t {OK} {key}: {value}')
                    return value
    #http requests
    g = rdflib.Graph()
    #foundValues = set()#maybe various values for one prop
    trouves = []#maybe various values each of the prop matching the regex pattern
    try:
        g.parse(uri)
        for predicateRegex in predicateRegexList:
            for s, p, o in g:
                if re.search(predicateRegex, p):
                    trouves.append(PropVal(p, o))#trouves is in the same order as predicateRegex (for property)
                    #foundValues.add(o)
    except:
        if re.search('/page/', uri):
            print(f'\t {NOK} URI contains _page_ string, not rdf data, human readable version')
        else:
            print(f'\t {NOK} no triples at this URI, check spelling')
        return "notFound"
    if not trouves:
        print(f'\t {NOK} predicate not found on URI')
        return "notFound"
    trouveInLang = filterPref(trouves)
    if trouveInLang:
        createNewURIrecord(uri, trouveInLang)
        return trouveInLang.val.toPython()
    #if none of the langPattern is found then
    default = trouves[0]#if nothing found in the pref languages, then get the first item, with property matching the first of the predicateRegexList
    createNewURIrecord(uri, default)
    print(f'\t {OK} {default.prop}: {default.val}')
    return default.val.toPython()

def updateKnownURILocalFile():
    if newKnownURIs:
        knownURIs.update(newKnownURIs)
        with open(KnownURIs_yamlFilepath, "w") as KnownURIsFile:
            output = yaml.dump(knownURIs, Dumper=yaml.CDumper)
            KnownURIsFile.write(output)
        print(f'updated URIlabel mapping in {KnownURIs_yamlFilepath}')

