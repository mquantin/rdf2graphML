import re
import rdflib
from rich import print
import yaml

OK = "[green]OK[/green]"
NOK = "[bold red]NOK[/bold red]"
foundURIlabels = {}
local_yamlFilepath = "URIlabels.yml"#history of mapping URI->label to limit the number of http requests 



with open(local_yamlFilepath) as URIlabelsFile:
    existingURIlabels = yaml.load(URIlabelsFile, Loader=yaml.CLoader)# dict with {URI:label} as {key:value}
    # for key, value in yaml_content.items():
    #     print(f"URI {key}: label {value}")



def filterLang(foundValues, langPattern):
    for label in foundValues:
        if label.language and label.language.startswith(langPattern):
            return label.toPython()

def getValue(uri, predicateRegex):
    if uri in existingURIlabels:
        return existingURIlabels[uri]["label"]
    g = rdflib.Graph()
    foundValues = set()#maybe various values for one prop
    try:
        g.parse(uri)
        for s, p, o in g:
            if re.search(predicateRegex, p):
                foundValues.add(o)
    except:
        print(f"{NOK} {uri}")
        if re.search('/page/', uri):
            print('\t URI contains _page_ string, not rdf data, human readable version')
        else:
            print('\t no triples at this URI, check spelling')
        return "notFound"
    if not foundValues:
        print(f"{NOK} {uri}")
        print('\t predicate not found on URI')
        return "notFound"
    for langPattern in ['fr', 'en', 'it']:#lang choices by order of pref
        valueinLang = filterLang(foundValues, langPattern)
        if valueinLang:
            print(f"{OK} {uri}")
            foundURIlabels[uri] = {"label":valueinLang, "lang": langPattern}
            print(f'\t trouvé: {valueinLang} ({langPattern})')
            return valueinLang
    #if none of the langPattern is found then
    default = foundValues.pop()#else return any value
    print(f"{OK} {uri}")
    foundURIlabels[uri] = {"label":default.toPython(), "lang": default.language}
    print(f'\t trouvé: {default.toPython()} ({default.language})')
    return default.toPython()

def updateURIlabelLocalFile():
    if foundURIlabels:
        existingURIlabels.update(foundURIlabels)
        with open(local_yamlFilepath, "w") as URIlabelFilePath:
            output = yaml.dump(existingURIlabels, Dumper=yaml.CDumper)
            URIlabelFilePath.write(output)
        print(f'updated URIlabel mapping in {local_yamlFilepath}')

