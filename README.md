# rdf2graphML
convert rdf files into a graphML file.  
Adds and fetch some info, hide and remove some other.

# General purpose
This script is done for creating visualization of rdf data.
It converts rdf data into graphML data.

The graphML data may be opened with various graph vizualisation softwares.  
I use [Cytoscape](https://cytoscape.org/).

# About the scripts
One part is done for converting RDF in graphML
Some assumption are done.  
The value of the following properties won't create new node.
- `rdf:type`
- `rdfs:label`
- any value that is not an URI but a dataType (literal, date, integer or whatever).

In these cases, instead of creating new nodes, a node attribute is added.
So it doesn't care if the property is declared as owl:objectProperty or owl:dataTypeProperty.

When a node is defined outside the local namespace (e.g. thesaurus URI), `prefLabel` attribute is fetched from that remote URI.


For example

```ttl
    <http://172.26.92.139/omeka-s/api/items/54> a crm:E12_Production ;
    # the class declaration never creates edge to another node. create node attribute "class"
    
        rdfs:label "Construction des grands moulins de Loire" ;
        # the rdfs:label never creates edge . create node attribute "label"
        
        dcterms:description "construction grands moulins de Loire" ;
        # string value: won't create an edge to a string node
        
        crm:p2_has_type <http://data.culture.fr/thesaurus/resource/ark:/67717/T96-820>,
        # creates an edge to another node, get prefLabel for it
        
        crm:P14_carried_out_by <http://viaf.org/viaf/21377236> ;
        # creates an edge to another node, get prefLLabel for it
```
