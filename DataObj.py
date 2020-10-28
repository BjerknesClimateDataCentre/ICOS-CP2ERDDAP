#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    The DataObj module is used to explore ICOS DataObjs and the corresponding
    data products. Since you need to know the "DataObj id" to create a DataObj
    object, convenience functions are provided:

    Example usage:

    from icoscp.DataObj import DataObj
    DataObj.getIdList() # returns a pandas data frame with all DataObj Id's'
    myDataObj = DataObj.get('DataObjId') # create a single statino object
    myList = DataObj.getList('AS') #  returns a list of Atmospheric DataObjs
"""

abc = {
    'citationString' : 'citation',
    'sha256sum' : 'toto'
}
# ----------------------------------------------
class DataObj():
    """ Create an ICOS DataObj object. This class intends to create
        an instance of DataObj, providing meta data as store in ICOS CP,
        including
        DataObjId, Name, country Code, GeoRegion(uri), label, comment, seeAlso

        Examples:
        import DataObj
        myList = DataObj.getList(['AS'])
        myDataObj = DataObj.get('HTM')

        DataObj.info()

        # extract single attribute
        DataObj.lat -> returns latitude as float
    """

    def __init__(self, sizeInBytes=None, sha256sum=None, citationString=None, name=None, doi=None,
                 nextVersionOf=None, dataSubmission=None, dataObjectSpec=None, dataAcquisition=None,
                 dataProduction=None, formatSpecificMetadata=None, keyword=None, variableName=None,
                 actualVariable=None, temporalResolution=None, spatialCoverage=None,
                 label=None, comment=None, seeAlso=None):
        """
        Initialize your DataObj either with NO arguments, or
        provide a list of arguments in the exact order how the
        attributes are listed
        [ DataObjID | DataObjName | countryCode | uriGeoRegion | label | comment |
         seeAlso ]

        """

        # Be aware, that attrList needs to be in the same ORDER as attributes
        # info
        self._sizeInBytes = sizeInBytes
        self._sha256sum = sha256sum
        self._citationString = citationString
        self._name = name
        self._doi = doi
        self._nextVersionOf = nextVersionOf
        self._dataSubmission = dataSubmission

        self._dataObjectSpec = dataObjectSpec
        self._dataAcquisition = dataAcquisition
        self._dataProduction = dataProduction
        self._formatSpecificMetadata = formatSpecificMetadata
        self._keyword = keyword
        self._variableName = variableName
        self._actualVariable = actualVariable
        self._temporalResolution = temporalResolution
        self._spatialCoverage = spatialCoverage

        self._label = label
        self._comment = comment
        self._seeAlso = seeAlso

        #self._uri = uri  # list, links to ressources, landing pages

    # super().__init__() # for subclasses
    # -------------------------------------
    @property
    def sizeInBytes(self):
        return self._sizeInBytes

    @sizeInBytes.setter
    def sizeInBytes(self, sizeInBytes):
        self._sizeInBytes = sizeInBytes

    # -------------------------------------
    @property
    def sha256sum(self):
        return self._sha256sum

    @sha256sum.setter
    def sha256sum(self, sha256sum):
        self._sha256sum = sha256sum

    # -------------------------------------
    @property
    def citationString(self):
        return self._citationString

    @citationString.setter
    def citationString(self, citationString):
        self._citationString = citationString

    # -------------------------------------
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    # -------------------------------------
    @property
    def doi(self):
        return self._doi

    @doi.setter
    def doi(self, doi):
        self._doi = doi

    # -------------------------------------
    @property
    def nextVersionOf(self):
        return self._nextVersionOf

    @nextVersionOf.setter
    def nextVersionOf(self, nextVersionOf):
        self._nextVersionOf = nextVersionOf

    # -------------------------------------
    @property
    def dataSubmission(self):
        return self._dataSubmission

    @dataSubmission.setter
    def dataSubmission(self, dataSubmission):
        self._dataSubmission = dataSubmission

    # -------------------------------------
    @property
    def dataObjectSpec(self):
        return self._dataObjectSpec

    @dataObjectSpec.setter
    def dataObjectSpec(self, dataObjectSpec):
        self._dataObjectSpec = dataObjectSpec

    # -------------------------------------
    @property
    def dataAcquisition(self):
        return self._dataAcquisition

    @dataAcquisition.setter
    def dataAcquisition(self, dataAcquisition):
        self._dataAcquisition = dataAcquisition

    # -------------------------------------
    @property
    def dataProduction(self):
        return self._dataProduction

    @dataProduction.setter
    def dataProduction(self, dataProduction):
        self._dataProduction = dataProduction

    # -------------------------------------
    @property
    def formatSpecificMetadata(self):
        return self._formatSpecificMetadata

    @formatSpecificMetadata.setter
    def formatSpecificMetadata(self, formatSpecificMetadata):
        self._formatSpecificMetadata = formatSpecificMetadata

    # -------------------------------------
    @property
    def keyword(self):
        return self._keyword

    @keyword.setter
    def keyword(self, keyword):
        self._keyword = keyword

    # -------------------------------------
    @property
    def variableName(self):
        return self._variableName

    @variableName.setter
    def variableName(self, variableName):
        self._variableName = variableName

    # -------------------------------------
    @property
    def actualVariable(self):
        return self._actualVariable

    @actualVariable.setter
    def actualVariable(self, actualVariable):
        self._actualVariable = actualVariable

    # -------------------------------------
    @property
    def temporalResolution(self):
        return self._temporalResolution

    @temporalResolution.setter
    def temporalResolution(self, temporalResolution):
        self._temporalResolution = temporalResolution

    # -------------------------------------
    @property
    def spatialCoverage(self):
        return self._spatialCoverage

    @spatialCoverage.setter
    def spatialCoverage(self, spatialCoverage):
        self._spatialCoverage = spatialCoverage

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



#def queryDataObjs(lastupdate='2020-01-01T00:00:00.000Z', endupdate='2020-01-05T00:00:00.000Z', product='icosOtcL1Product_v2', lastVersion=False):
def queryDataObjs(lastupdate='', endupdate='', product='', lastVersion=False, dobj=''):
    """
    select in ICOS CP, all data object
    :param lastupdate: date since last update ( '2020-01-01T00:00:00.000Z' )
    :param product: select this product type
    :param lastVersion: select only last release
    :return:
    """

    from SPARQLWrapper import SPARQLWrapper2

    filterLastUpDate=''
    if lastupdate:
        filterLastUpDate="FILTER( ?submTime >= '%s'^^xsd:dateTime )" % lastupdate

    filterEndUpDate=''
    if endupdate:
        filterEndUpDate="FILTER( ?submTime <= '%s'^^xsd:dateTime )" % endupdate

    filterProdcut=''
    if  product:
        filterProdcut="VALUES ?spec {<http://meta.icos-cp.eu/resources/cpmeta/%s>}" % product

    filterLastVersion=''
    if lastVersion:
        filterLastVersion="FILTER NOT EXISTS {[] cpmeta:isNextVersionOf ?dataObj}"

    filterDobj=''
    if dobj:
        filterDobj="VALUES ?dataObj {<%s>}" % dobj

    queryString="""
        prefix cpmeta: <http://meta.icos-cp.eu/ontologies/cpmeta/>
        prefix otcmeta: <http://meta.icos-cp.eu/ontologies/otcmeta/>
        prefix prov: <http://www.w3.org/ns/prov#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix xsd: <http://www.w3.org/2001/XMLSchema#>

        select ?dataObj ?sizeInBytes ?sha256sum ?citationString ?name ?doi ?nextVersionOf ?dataSubmission 
               ?dataObjectSpec ?datAcquisition ?dataProduction ?formatSpecificMetadata ?keyword ?variableName 
               ?actualVariable ?temporalResolution ?spatialCoverage ?label ?comment ?seeAlso
        where {
            %s #VALUES ?dataObj {<http://meta.icos-cp.eu/object>}
            %s #VALUES ?spec {<http://meta.icos-cp.eu/resources/cpmeta/icosOtcL1Product_v2>}
            ?dataObj cpmeta:hasObjectSpec ?spec . # restiction property for DataObject and/or SimpleDataObject
            ?dataObj cpmeta:wasSubmittedBy [
                prov:endedAtTime ?submTime ;
                prov:wasAssociatedWith ?submitter
                ] .
            %s #FILTER( ?submTime <= '2020-02-01T00:00:00.000Z'^^xsd:dateTime )
            %s #FILTER( ?submTime >= '2020-01-01T00:00:00.000Z'^^xsd:dateTime )
            %s #FILTER NOT EXISTS {[] cpmeta:isNextVersionOf ?dataObj}
             
            OPTIONAL { ?dataObj cpmeta:hasSizeInBytes ?sizeInBytes .}          # as subClassOf DataObject
            OPTIONAL { ?dataObj cpmeta:hasSha256sum ?sha256sum .}               # as subClassOf DataObject
            OPTIONAL { ?dataObj cpmeta:hasCitationString ?citationString .}     # as subClassOf DataObject
            OPTIONAL { ?dataObj cpmeta:hasName ?name .}
            OPTIONAL { ?dataObj cpmeta:hasDoi ?doi .}
            OPTIONAL { ?dataObj cpmeta:isNextVersionOf ?nextVersionOf .}

            OPTIONAL { ?dataObj cpmeta:wasSubmittedBy ?dataSubmission .}           # as subClassOf DataObject
            OPTIONAL { ?dataObj cpmeta:hasObjectSpec ?dataObjectSpec .}       # domain

            OPTIONAL { ?dataObj cpmeta:wasAcquiredBy ?datAcquisition .}       # domain
            OPTIONAL { ?dataObj cpmeta:wasProducedBy ?dataProduction .}       # domain

            OPTIONAL { ?dataObj cpmeta:hasFormatSpecificMetadata ?formatSpecificMetadata .}
            OPTIONAL { ?dataObj cpmeta:hasKeyword ?keyword . }
            OPTIONAL { ?dataObj cpmeta:hasVariableName ?variableName .}
            OPTIONAL { ?dataObj cpmeta:hasActualVariable ?actualVariable .}
            OPTIONAL { ?dataObj cpmeta:hasTemporalResolution ?temporalResolution .}
            OPTIONAL { ?dataObj cpmeta:hasSpatialCoverage ?spatialCoverage .}

            OPTIONAL { ?dataObj rdfs:label ?label .}
            OPTIONAL { ?dataObj rdfs:comment ?comment .}
            OPTIONAL { ?dataObj rdfs:seeAlso ?seeAlso .}
        }
        limit 10
    """ % (filterDobj, filterProdcut, filterLastUpDate, filterEndUpDate, filterLastVersion)

    sparql = SPARQLWrapper2("https://meta.icos-cp.eu/sparql")

    sparql.setQuery(queryString)

    return sparql.query()

def load_data():
    """

    :return:
    """
    import requests
    r = requests.get('https://data.icos-cp.eu/objects/8Pj-v7cmVZUm-8j0zFG96USA')

    print(r.text)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(e)


def download(url,o):
    """

    curl -JO -H "Cookie: CpLicenseAcceptedFor=PID" URL

    :param url:
    :return:
    """
    import requests
    from requests.exceptions import HTTPError
    #from requests.auth import HTTPDigestAuth

    #url = 'https://data.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z'
    pid = url.split("/")[-1]
    cookies = dict(CpLicenseAcceptedFor=pid)
    # Fill in your details here to be posted to the login form.
    #user, pswd = 'julien.paul@uib.no', 'Lw9ucQr5EEQ9SaK'

    ## Use 'with' to ensure the session context is closed after use.
    with requests.Session() as s:
        #LOGIN_URL = 'https://cpauth.icos-cp.eu/login/'
        #p = s.post(LOGIN_URL, data={user : pswd})
        ## print the html returned or something more intelligent to see if it's a successful login page.
        #print('html return ')#, p.text)

        try:
            # an authorised request.
            #r = s.get(url, auth=(user,pswd), stream=True)
            #r = requests.get(url, auth=HTTPDigestAuth(user, pswd), stream=True)
            print(url,type(url))
            print(cookies)
            r = s.get(str(url), cookies=cookies, stream=True)
            # If the response was successful, no Exception will be raised
            r.raise_for_status()
        except HTTPError as http_err:
            # https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')
            # etc...
            print('download file ',url,' on ',o)
            with open(o, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)


def renameKeyDic(mydict):
    """
    renaming dictionary keys:
    :return:
    """
    for oldKey, newKey in abc.items():
        mydict = dict((newKey, v) if k == oldKey else (k, v) for k, v in mydict.items())
    return mydict

def get_meta(lastupdate='', endupdate='', product='', lastVersion=False, dobj=''):
    """

    :return: dataObjs' dictionary
    """
    # init empty dict
    dataObjs={}

    res=queryDataObjs(lastupdate, endupdate, product, lastVersion, dobj)
    for result in res.bindings:
        uri=None
        sizeInBytes=None
        sha256sum=None
        citationString=None
        name=None
        doi=None
        nextVersionOf=None
        dataSubmission=None
        dataObjectSpec=None
        dataAcquisition=None
        dataProduction=None
        formatSpecificMetadata=None
        keyword=None
        variableName=None
        actualVariable=None
        temporalResolution=None
        spatialCoverage=None
        label=None
        comment=None
        seeAlso=None
        if "dataObj" in result:
            print('dataObj: %s: %s' % (result["dataObj"].type, result["dataObj"].value))
            uri=result["dataObj"].value
        if "sizeInBytes" in result:
            print('sizeInBytes: %s: %s' % (result["sizeInBytes"].type, result["sizeInBytes"].value))
            sizeInBytes=result["sizeInBytes"].value
        if "sha256sum" in result:
            print('sha256sum: %s: %s' % (result["sha256sum"].type, result["sha256sum"].value))
            sha256sum=result["sha256sum"].value
        if "citationString" in result:
            print('citationString: %s: %s' % (result["citationString"].type, result["citationString"].value))
            citationString=result["citationString"].value
        if "name" in result:
            print('name: %s: %s' % (result["name"].type, result["name"].value))
            name=result["name"].value
        if "doi" in result:
            print('doi: %s: %s' % (result["doi"].type, result["doi"].value))
            doi=result["doi"].value
        if "nextVersionOf" in result:
            print('nextVersion: %s: %s' % (result["nextVersionOf"].type, result["nextVersionOf"].value))
            nextVersionOf=result["nextVersionOf"].value
        if "dataSubmission" in result:
            print('dataSubmission: %s: %s' % (result["dataSubmission"].type, result["dataSubmission"].value))
            dataSubmission=result["dataSubmission"].value
        if "dataObjectSpec" in result:
            print('dataObjectSpec: %s: %s' % (result["dataObjectSpec"].type, result["dataObjectSpec"].value))
            dataObjectSpec=result["dataObjectSpec"].value
        if "dataAcquisition" in result:
            print('dataAcquisition: %s: %s' % (result["dataAcquisition"].type, result["dataAcquisition"].value))
            dataAcquisition=result["dataAcquisition"].value
        if "dataProduction" in result:
            print('dataProduction: %s: %s' % (result["dataProduction"].type, result["dataProduction"].value))
            dataProduction=result["dataProduction"].value
        if "formatSpecificMetadata" in result:
            print('formatSpecificMetadata: %s: %s' % (result["formatSpecificMetadata"].type, result["formatSpecificMetadata"].value))
            formatSpecificMetadata=result["formatSpecificMetadata"].value
        if "keyword" in result:
            print('keyword: %s: %s' % (result["keyword"].type, result["keyword"].value))
            keyword=result["keyword"].value
        if "variableName" in result:
            print('variableName: %s: %s' % (result["variableName"].type, result["variableName"].value))
            variableName=result["variableName"].value
        if "actualVariable" in result:
            print('actualVariable: %s: %s' % (result["actualVariable"].type, result["actualVariable"].value))
            actualVariable=result["actualVariable"].value
        if "temporalResolution" in result:
            print('temporalResolution: %s: %s' % (result["temporalResolution"].type, result["temporalResolution"].value))
            temporalResolution=result["temporalResolution"].value
        if "spatialCoverage" in result:
            print('spatialCoverage: %s: %s' % (result["spatialCoverage"].type, result["spatialCoverage"].value))
            spatialCoverage=result["spatialCoverage"].value

        if "label" in result:
            print('label: %s: %s' % (result["label"].type, result["label"].value))
            label=result["label"].value
        if "comment" in result:
            print('comment: %s: %s' % (result["comment"].type, result["comment"].value))
            comment=result["comment"].value
        if "seeAlso" in result:
            print('seeAlso: %s: %s' % (result["seeAlso"].type, result["seeAlso"].value))
            seeAlso=result["seeAlso"].value

        result['uri'] = result.pop("dataObj")

        print(result)
        print('\nrename attribute\n---------\n')
        dataObjs[uri]=renameKeyDic(result)
        #dataObjs[uri]=DataObj(sizeInBytes, sha256sum, citationString, name, doi, nextVersionOf, dataSubmission,
        #                      dataObjectSpec, dataAcquisition, dataProduction, formatSpecificMetadata, keyword,
        #                      variableName, actualVariable, temporalResolution, spatialCoverage,
        #                      label, comment, seeAlso)

    return dataObjs

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dobj = 'https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z'

    print('\nquery on last submission\n')
    dataObjs = get_meta(lastupdate='2020-01-01T00:00:00.000Z', endupdate='2020-08-05T00:00:00.000Z',
                        product='icosOtcL1Product_v2', lastVersion=True)
    for k, v in dataObjs.items():
        for kk, vv in v.items():
            print(kk, ' : ','type:',vv.type,'value:',vv.value)

    print('\nquery on one dataObj\n')
    dataObjs = get_meta(dobj=dobj)
    for k, v in dataObjs.items():
        for kk, vv in v.items():
            print(kk, ' : ','type:',vv.type,'value:',vv.value)

    #for k,v in dataObjs.items():
    #    print(k,' : ',v.sha256sum,v.name,v.doi,v.variableName, v.nextVersionOf)

    print('\n\n')
    #url = 'https://data.icos-cp.eu/objects/8Pj-v7cmVZUm-8j0zFG96USA'   # 26NA_NRT_20190327.csv
    url = 'https://data.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z'
    out='toto.csv'
    #download(url,out)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
