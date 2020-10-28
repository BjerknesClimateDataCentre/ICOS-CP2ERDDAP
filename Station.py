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
class Station():
    """ Create an ICOS Station object. This class intends to create
        an instance of station, providing meta data as store in ICOS CP,
        including
        stationId, Name, country Code, GeoRegion(uri), label, comment, seeAlso

        Examples:
        import station
        myList = station.getList(['AS'])
        myStation = station.get('HTM')

        station.info()

        # extract single attribute
        station.lat -> returns latitude as float
    """

    def __init__(self, stationId=None, stationName=None, countryCode=None, uriGeoRegion=None,
                 label=None, comment=None, seeAlso=None):
        """
        Initialize your Station either with NO arguments, or
        provide a list of arguments in the exact order how the
        attributes are listed
        [ stationID | stationName | countryCode | uriGeoRegion | label | comment |
         seeAlso ]

        """

        # Be aware, that attrList needs to be in the same ORDER as attributes
        # info
        self._stationId = stationId         # shortName like HTM or SE-NOR
        self._stationName = stationName            # longName
        self._countryCode = countryCode
        self._uriGeoRegion = uriGeoRegion
        self._label = label
        self._comment = comment
        self._seeAlso = seeAlso

        #self._uri = uri  # list, links to ressources, landing pages

    # super().__init__() # for subclasses
    # -------------------------------------
    @property
    def stationId(self):
        return self._stationId

    @stationId.setter
    def stationId(self, stationId):
        self._stationId = stationId

    # -------------------------------------
    @property
    def stationName(self):
        return self._stationName

    @stationName.setter
    def stationName(self, stationName):
        self._stationName = stationName

    # -------------------------------------
    @property
    def countryCode(self):
        return self._countryCode

    @countryCode.setter
    def countryCode(self, countryCode):
        self._countryCode = countryCode

    # -------------------------------------
    @property
    def project(self):
        return self._uriGeoRegion

    @project.setter
    def project(self, uriGeoRegion):
        self._uriGeoRegion = uriGeoRegion

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
        
        
        select ?station ?uriGeoRegion ?stationId ?name ?countryCode ?label ?comment ?seeAlso
        where {
           ?station rdf:type/rdfs:subClassOf*  <http://meta.icos-cp.eu/ontologies/otcmeta/Station> .
        
           OPTIONAL { ?station otcmeta:hasGeoRegion ?uriGeoRegion .}    
           OPTIONAL { ?station otcmeta:hasStationId ?stationId .}       
           OPTIONAL { ?station otcmeta:hasName ?name .}                 
           OPTIONAL { ?station otcmeta:countryCode ?countryCode .}      
        
           OPTIONAL { ?station rdfs:label ?label .}
           OPTIONAL { ?station rdfs:comment ?comment .}
           OPTIONAL { ?station rdfs:seeAlso ?seeAlso .}
        }
        limit 10
    """

    sparql = SPARQLWrapper2("https://meta.icos-cp.eu/sparql")

    sparql.setQuery(queryString)

    return sparql.query()

def get_meta():
    """

    get all stations, and their attributes from ICOS CP

    :return: stations' dictionary
    """
    # init empty dict
    stations = {}

    res = queryStations()
    for result in res.bindings:
        uri = None
        stationId = None
        uriGeoRegion = None
        stationName = None
        countryCode = None
        label = None
        comment = None
        seeAlso = None
        if "station" in result:
            #print('station: %s: %s' % (result["station"].type, result["station"].value))
            uri = result["station"].value
        if "stationId" in result:
            #print('stationId: %s: %s' % (result["stationId"].type, result["stationId"].value))
            stationId = result["stationId"].value
        if "uriGeoRegion" in result:
            #print('uriGeoRegion: %s: %s' % (result["uriGeoRegion"].type, result["uriGeoRegion"].value))
            uriGeoRegion = result["uriGeoRegion"].value
        if "name" in result:
            #print('name: %s: %s' % (result["name"].type, result["name"].value))
            stationName = result["name"].value
        if "countryCode" in result:
            #print('countryCode: %s: %s' % (result["countryCode"].type, result["countryCode"].value))
            countryCode = result["countryCode"].value
        if "label" in result:
            #print('label: %s: %s' % (result["label"].type, result["label"].value))
            label = result["label"].value
        if "comment" in result:
            #print('comment: %s: %s' % (result["comment"].type, result["comment"].value))
            comment = result["comment"].value
        if "seeAlso" in result:
            #print('seeAlso: %s: %s' % (result["seeAlso"].type, result["seeAlso"].value))
            seeAlso = result["seeAlso"].value

        #stations[uri] = Station(stationId, stationName, countryCode, uriGeoRegion, label, comment, seeAlso)

        result.pop("station")
        stations[uri]=result

    return stations

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    stations=get_meta()

    for k,v in stations.items():
        for kk, vv in v.items():
            print(kk, ' : ','type:',vv.type,'value:',vv.value)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
