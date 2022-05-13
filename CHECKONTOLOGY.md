# What to do when checkOntology detect changes in ICOS CP

## Re-run `checkOntology` with option `--write_ontology` 

`python3 -m icp2edd.checkOntology --write_ontology`

then compare `cpmeta_icp_*.txt` and `cpmeta_edd_*.txt` files.  
- cpmeta_icp_*.txt : informations about what is on ICOS CP
- cpmeta_edd_*.txt : informations about what is on icp2edd python package

## Check on SPARQL endpoint
On [ICOS-CP SPARQL endpoint](https://meta.icos-cp.eu/sparqlclient/?type=TSV%20or%20Turtle) check urls.

example:  
`describe <url/Class>`

> Note: use `return type: TSV or Turtle`

## Namespace
list of namespaces (and url) use on ICOS-CP and on icp2edd python package.  
`vim -d cpmeta_icp_namespace.txt cpmeta_edd_namespace.txt`

If any namespace is missing on icp2edd python package:
- add it in `_ns` dictionary in `icp2edd/icpobj/icpObj.py`.
> Note: It may have more namespace on python package than on ICOS CP, it does not matter.

## Class
list of classes (and subclasses) use on ICOS-CP and on icp2edd python package.  
`vim -d cpmeta_icp_classes.txt cpmeta_edd_classes.txt`

If any class (NewClass) is missing on icp2edd python package:
- create a file (`newClass.py`) on `icp2edd/icpobj/X` where X is the namespace
> Note: if the namespace directory does not exist, create it and add in a file `__init__.py` (filled as in other namespace).

check on [ICOS-CP SPARQL endpoint](https://meta.icos-cp.eu/sparqlclient/?type=TSV%20or%20Turtle)   
`describe <NewClass>`  
from result:
- list all SubClass of the NewClass  
    `<SubClass> rdfs:subClassOf <NewClass>` 

    add them in `newClass.py` as comment to keep a track of it.

- list all properties of the NewClass  
    `<property> rdfs:domain <NewClass>`

    check each property on [ICOS-CP SPARQL endpoint](https://meta.icos-cp.eu/sparqlclient/?type=TSV%20or%20Turtle)

    if the property is a subproperty of another  
    `<subProperty> rdfs:subPropertyOf <property>`
    
    then
    - add it in `hasSubProp` dictionary in `icpobj/subproperties.py`, as subproperty of <property> 
    - add it in `newClass.py` in `_attr` dictionary, as comment to keep track of it.

    else
    - add it in `newClass.py` in `_attr` dictionary.

## Property
`vim -d cpmeta_icp_properties.txt cpmeta_edd_properties.txt`  
`vim -d cpmeta_icp_classprop.txt cpmeta_edd_classprop.txt`

> **Note:** first focus on part '0'

check on [ICOS-CP SPARQL endpoint](https://meta.icos-cp.eu/sparqlclient/?type=TSV%20or%20Turtle)  
`describe <property>`  
from result:  

if the property is a subproperty of another  
`<subProperty> rdfs:subPropertyOf <property>`

then
- add it in `hasSubProp` dictionary in `icpobj/subproperties.py` 
- add it in `class.py` in `_attr` dictionary, as comment to keep track of it.  
    - where `class.py` is the class on which the property came from.

else  
    `<property> a owl:ObjectProperty`  
    `rdfs:domain <Class>`

- add it in `class.py` in `_attr` dictionary.
    - where `class.py` is the class on which the property came from.