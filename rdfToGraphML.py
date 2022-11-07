
import rdflib
import networkx as nx
from getURIvalue import getValue
import re

## CONSTANTS ##
rdf_file_path = "/home/matthieu/Downloads/omekaRDF/files/items.ttl"
graphML_file_path = '/home/matthieu/Downloads/omekaRDF/files/items.graphml'
local_nameSpace_dns =  'http://172.26.92.139'# if not in this nameSpace, fetch data values from URI

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
            nodeObj['label'] = getValue(n, 'skos/core#prefLabel')#|http://www.geonames.org/ontology#name')

def feedGraph():
    for s, p, o in rdf_graph.triples((None, None, None)):
        # The .toPython() method converts rdflib objects into objects
        #  that any Python module can understand (e.g. str, int, float).

        predic = prefixForURI(p)

        #following cases won't create a new node for the object but only a attribute to the actual nodes
        # this simplifies the graph
        if predic == 'rdfs:label':
            graph.add_node(s.toPython(), label=o.toPython())
        elif predic == 'rdf:type':
            graph.add_node(s.toPython(), type=prefixForURI(o))#with only prefix not whole URI
        elif not re.match('https?://', o.toPython()):
            #case other object not an other node URI but a simple string or integer
            graph.add_node(s.toPython())
            graph.nodes[s.toPython()][predic] = o.toPython()
        #case edge to another (entity)
        else:
            graph.add_edge(s.toPython(), o.toPython(), predicate=predic)
    print(f'Added {graph.order()} nodes and {graph.size()} edges to the graph')

feedGraph()
moreNodeAttributes()

nx.write_graphml(graph, graphML_file_path)
print(f'wrote output in {graphML_file_path}')
