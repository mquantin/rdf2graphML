
import rdflib
import networkx as nx
from getURIvalue import getValue, updateURIlabelLocalFile
import re
from collections import defaultdict

## CONSTANTS ##
rdf_file_path = "/Users/ls2n/Documents/utils/omekas2rdf/files/items.ttl"
graphML_file_path = '/Users/ls2n/Downloads/itemscap44.graphml'
local_nameSpace_dns =  'https://cap44.univ-nantes.fr'#if not in this nameSpace, fetch data values from URI

rdf_graph = rdflib.Graph()
rdf_graph.parse(rdf_file_path)
graph = nx.DiGraph()    # RDF properties are directed.

def prefixForURI(URI):
    #only for displaying shorter strings in graph visualization
    return URI.n3(rdf_graph.namespace_manager)#with only prefix not whole URI

def moreNodeAttributes():
    for n, atts in graph.nodes(data=True):
        nodeObj = graph.nodes[n]
        if n.startswith(local_nameSpace_dns):
            nodeObj['local'] = True
        else:
            nodeObj['local'] = False
            nodeObj['label'] = getValue(n, 'skos/core#prefLabel|geonames.org/ontology#alternateName|geonames.org/ontology#name')

def feedGraph():
    labelCandidates = defaultdict(list)
    for s, p, o in rdf_graph.triples((None, None, None)):
        # The .toPython() method converts rdflib objects into objects
        #  that any Python module can understand (e.g. str, int, float).
        predic = prefixForURI(p)
        #following cases won't create a new node for the object but only a attribute to the actual nodes
        # this simplifies the graph
        # create a label attribute with a short content if available
        accepted_labels = {'bibo:shortTitle', 'skos:prefLabel', 'rdfs:label', 'skos:altLabel'}
        if predic in accepted_labels:
            labelCandidates[s].append(o.toPython())
        if predic == 'rdf:type':
            graph.add_node(s.toPython(), type=prefixForURI(o))#with only prefix not whole URI
        elif not re.match('https?://', o.toPython()):
            #case other object not an other node URI but a simple string or integer
            graph.add_node(s.toPython())
            graph.nodes[s.toPython()][predic] = o.toPython()
        #case edge to another (entity)
        else:
            graph.add_edge(s.toPython(), o.toPython(), predicate=predic)
    for sujet, labels in labelCandidates.items():
        graph.add_node(sujet.toPython(), label=min(labels, key=len))
    print(f'Added {graph.order()} nodes and {graph.size()} edges to the graph')


feedGraph()
moreNodeAttributes()
updateURIlabelLocalFile()

nx.write_graphml(graph, graphML_file_path)
print(f'wrote output in {graphML_file_path}')
