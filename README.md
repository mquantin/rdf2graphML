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
- rdf:type
- rdfs:label
- any value that is not an URI but a string

Instead of creating new nodes, a node attribute is added.

For example

'''ttl
<http://172.26.92.139/omeka-s/api/items/54> a crm:E12_Production ;
    rdfs:label "Construction des grands moulins de Loire" ;
    dcterms:description "construction grands moulins de Loire" ;
    crm:p2_has_type <http://data.culture.fr/thesaurus/resource/ark:/67717/T96-820>,
    crm:P108_has_produced "Grands moulins de Loire" ;
    crm:P14_carried_out_by <http://viaf.org/viaf/21377236> ;
    crm:P4_has_time-span <http://172.26.92.139/omeka-s/api/items/24>,
        "1895-1934" ;
    crm:P55_has_current_location <http://172.26.92.139/omeka-s/api/items/33> ;
    crm:P65_shows_visual_item "photo" ;
    crm:P7_took_place_at <http://172.26.92.139/omeka-s/api/items/51>,

'''
