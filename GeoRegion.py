#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    The Station module is used to explore ICOS stations and the corresponding
    data products. Since you need to know the "station id" to create a station
    object, convenience functions are provided:

    Example usage:

    from icoscp.station import station
    station.getIdList() # returns a pandas data frame with all station Id's'
    myStation = station.get('StationId') # create a single statino object
    myList = station.getList('AS') #  returns a list of Atmospheric stations
"""

# ----------------------------------------------
class GeoRegion():
    """ Create an ICOS Station object. This class intends to create
        an instance of GeoRegion, providing meta data as store in ICOS CP,
        including
        label, comment, seeAlso

        Examples:
        import station
        myList = station.getList(['AS'])
        myStation = station.get('HTM')

        station.info()

        # extract single attribute
        station.lat -> returns latitude as float
    """

    def __init__(self, label=None, comment=None, seeAlso=None):
        """
        Initialize your Station either with NO arguments, or
        provide a list of arguments in the exact order how the
        attributes are listed
        [ stationID | stationName | countryCode | uriGeoRegion | label | comment |
         seeAlso ]

        """

        # Be aware, that attrList needs to be in the same ORDER as attributes
        # info
        self._label = label
        self._comment = comment
        self._seeAlso = seeAlso


    # super().__init__() # for subclasses
    # -------------------------------------
    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = label
    # -------------------------------------
    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, comment):
        self._comment = comment
    # -------------------------------------
    @property
    def seeAlso(self):
        return self._seeAlso

    @seeAlso.setter
    def seeAlso(self, seeAlso):
        self._seeAlso = seeAlso

def queryStations():
    from SPARQLWrapper import SPARQLWrapper2

    queryString="""
        prefix cpmeta: <http://meta.icos-cp.eu/ontologies/cpmeta/>
        prefix otcmeta: <http://meta.icos-cp.eu/ontologies/otcmeta/>
        prefix prov: <http://www.w3.org/ns/prov#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>


        select ?geoRegion ?label ?comment ?seeAlso
        where {
           ?geoRegion rdf:type/rdfs:subClassOf*  <http://meta.icos-cp.eu/ontologies/otcmeta/GeoRegion> .

           OPTIONAL { ?geoRegion rdfs:label ?label .}
           OPTIONAL { ?geoRegion rdfs:comment ?comment .}
           OPTIONAL { ?geoRegion rdfs:seeAlso ?seeAlso .}
        }
        limit 10
    """

    sparql = SPARQLWrapper2("https://meta.icos-cp.eu/sparql")

    sparql.setQuery(queryString)

    return sparql.query()

def get_meta():
    """

    :return: geoRegions' dictionary
    """
    # init empty dict
    geoRegions={}

    res=queryStations()
    for result in res.bindings:
        uri=None
        label=None
        comment=None
        seeAlso=None
        if "geoRegion" in result:
            #print('geoRegion: %s: %s' % (result["geoRegion"].type, result["geoRegion"].value))
            uri=result["geoRegion"].value
        if "label" in result:
            #print('label: %s: %s' % (result["label"].type, result["label"].value))
            label=result["label"].value
        if "comment" in result:
            #print('comment: %s: %s' % (result["comment"].type, result["comment"].value))
            comment=result["comment"].value
        if "seeAlso" in result:
            #print('seeAlso: %s: %s' % (result["seeAlso"].type, result["seeAlso"].value))
            seeAlso=result["seeAlso"].value

        #geoRegions[uri]=GeoRegion(label, comment, seeAlso)

        #print("\n--------\n")
        result.pop("geoRegion")
        geoRegions[uri]=result

    return geoRegions

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    geoRegions=get_meta()

    for k,v in geoRegions.items():
        for kk, vv in v.items():
            print(kk, ' : ','type:',vv.type,'value:',vv.value)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
