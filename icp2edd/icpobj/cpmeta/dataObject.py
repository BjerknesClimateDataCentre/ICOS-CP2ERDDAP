#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# dataObject.py

"""
    The dataObject module is used to explore ICOS CP cpmeta::DataObjects' metadata.

    Example usage:

    from cpmeta import DataObject

    dataObjects = DataObject()        # initialise ICOS CP DataObject object
    dataObjects.get_meta()            # get dataObjects' metadata from ICOS CP
    dataObjects.show()                # print dataObjects' metadata
    dataobjects.download()            # download every files associated with dataobjects selected
"""

# --- import -----------------------------------
# import from standard lib
import logging
import re
import traceback
from pathlib import Path
from pprint import pformat

# import from other lib
import requests
from requests.exceptions import HTTPError
from SPARQLWrapper.SmartWrapper import Value as SmartWrapperValue

# import from my project
import icp2edd.setupcfg as setupcfg
from icp2edd.icpobj.cpmeta.staticObject import StaticObject

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)

# object attributes' dictionary with RDF 'property' as key and RDF 'object' as value
#   RDF triples: 'subject' + 'property/predicate' + 'object/value'
# {'property/predicate': 'object/value'}
# Note: 'object/value' will be the output attribute name
_attr = {
    "cpmeta:hasObjectSpec": "specification",  # cpmeta/DataObjectSpec
    "cpmeta:hasFormatSpecificMetadata": "format",  # rdfs:Literal
    # subproperty {
    # "wdcgg:CONTACT%20POINT": "contact_point",  #
    # "wdcgg:CONTRIBUTOR": "contributor",  #
    # "wdcgg:MEASUREMENT%20METHOD": "measurement_method",  #
    # "wdcgg:MEASUREMENT%20SCALE": "measurement_scale",  #
    # "wdcgg:MEASUREMENT%20UNIT": "measurement_unit",  #
    # "wdcgg:OBSERVATION%20CATEGORY": "observation_category",  #
    # "wdcgg:PARAMETER": "parameter",  #
    # "wdcgg:SAMPLING%20TYPE": "sampling_type",  #
    # "wdcgg:TIME%20INTERVAL": "time_interval",  #
    # }
    "cpmeta:hasKeyword": "keyword",  # xsd:string
    "cpmeta:hasKeywords": "keywords",  # xsd:string
    "cpmeta:hasActualVariable": "variable",
    "cpmeta:hasSpatialCoverage": "location",  # cpmeta/SpatialCoverage
    "cpmeta:hasTemporalResolution": "temporal_resolution",  # xsd:string
    "cpmeta:hasVariableName": "variable_name",  # xsd:string
    "terms:license": "license",  #
}
# list of equivalent class
_equivalentClass = ["cpmeta.SimpleDataObject", "cpmeta.SpatialDataObject"]


# ----------------------------------------------
class DataObject(StaticObject):
    """
    >>> t.getMeta()
    >>> t.show(True)
    >>> t._queryString()
    """

    def __init__(
        self,
        limit=None,
        submfrom=None,
        submuntil=None,
        product=None,
        lastversion=None,
        uri=None,
    ):
        """initialise instance of DataObject(StaticObject).

        It will be used to set up a sparql query, and get all metadata of DataObject from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select DataObject:
        - submitted from 'submfrom'
        - submitted until 'submuntil'
        - of data type 'product'
        - only from the 'lastversion'
        - with ICOS CP 'uri'

        Example:
            DataObject(submfrom='2020-01-01T00:00:00.000Z',
                       submuntil='2020-01-05T00:00:00.000Z',
                       product='icosOtcL1Product_v2',
                       lastversion=False )

        :param limit: number of returned results
        :param submfrom: submitted from date ( '2020-01-01T00:00:00.000Z' )
        :param submuntil: submitted until date ( '2020-01-01T00:00:00.000Z' )
        :param product: select this product type ('icosOtcL1Product_v2'), it could be a list
        :param lastversion: select only last release [True,False]
        :param uri: ICOS CP URI ('https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z')
        """
        super().__init__()
        # set up class/instance variables
        self._uri = uri
        self._limit = limit
        self._from = submfrom
        self._until = submuntil
        self._product = product
        self._lastversion = lastversion

        # inherit properties
        self._inherit = {**self.attr}

        if isinstance(_attr, dict):
            # keep own properties
            self._attr = _attr
            # merge own and inherit properties.
            # Note:  .attr's values are overwritten by the self.attr's
            self.attr = {**self._attr, **self._inherit}
            # add subproperties
            for prop in self.attr:
                self._addSubProperties(prop)

        if isinstance(_equivalentClass, list):
            self._equivalentClass = _equivalentClass

        # object type URI
        self._object = "http://meta.icos-cp.eu/ontologies/cpmeta/DataObject"

        #
        self._objtype = None
        if self._object is not None:
            self.objtype = self._getObjectType()

        # get instance name
        (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
        self._instance_name = text[: text.find("=")].strip()

    def getMeta(self):
        """
        Add 'doi' to attributes, if need be
        """
        super().getMeta()
        #
        for uri in list(self._uri):
            _ = self.meta[uri]
            # if no doi create one
            if "doi" not in _.keys():
                url = "https://hdl.handle.net/11676/"
                binding = {"value": url + str(Path(uri).stem), "type": "literal"}
                _["doi"] = [SmartWrapperValue("doi", binding)]
            #
            _logger.info(f"self.meta[{uri}].doi: {_['doi']}")

    def download(self):
        """download file associated to dataobject

        download every file associated with the dataobjects selected on ICOS CP,
        and store them on a temporary directory named by the dataset 'name'

        :return: dictionary with csv file as key, and dirout as value

        >>> t.getMeta()
        >>> output = t.download()
        download file  https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z  on
            .../58GS20190711_SOCAT_enhanced/58GS20190711_SOCAT_enhanced.csv
        """
        d = {}
        for uri, binding in self.meta.items():
            # there is at least one binding covering the optional "opt", too
            # uri = binding['uri'].value  # Warning do not convert to Path (https:// => https./)
            pid = uri.split("/")[-1]
            # Warning: linked to staticObject.py 'cpmeta:hasName': 'filename'
            if "filename" not in binding:
                _logger.critical(
                    f"can not find 'filename' attribute in binding.\n "
                    f"Check value of 'cpmeta:hasName' in StaticObject"
                )

            if len(binding["filename"]) > 1:
                _logger.critical(
                    f"several filenames associated to one uri, meta:\n{pformat(binding)}"
                )
            else:
                # replace white space(s) by underscore
                filename = Path(re.sub("\s+", "_", binding["filename"][0].value))
                stemname = filename.stem

                pattern = re.compile("(.*)(\d{8})(\D*)")
                result = re.match(pattern, stemname)
                dirout = setupcfg.datasetCsvPath / result[1] / stemname
                try:
                    dirout.mkdir(parents=True)
                except FileExistsError:
                    # directory already exists
                    pass

                url = str(uri).replace("meta", "data")
                fileout = dirout / filename
                if filename not in d:
                    # download
                    _doi = None
                    if "doi" in binding:
                        _doi = binding["doi"][0].value
                    else:
                        _logger.debug(f"can not find 'doi' attribute for {filename}.")

                    d[filename] = {"path": dirout, "doi": _doi}

                    cookies = dict(CpLicenseAcceptedFor=pid)
                    # Fill in your details here to be posted to the login form.
                    # user, pswd = 'julien.paul at uib.no', 'Lw9ucQr5EEQ9SaK'

                    # Use 'with' to ensure the session context is closed after use.
                    _logger.info(f"downloading file {uri} on {fileout}")
                    with requests.Session() as s:
                        # LOGIN_URL = 'https://cpauth.icos-cp.eu/login/'
                        # p = s.post(LOGIN_URL, data={user : pswd})
                        # print the html returned or something more intelligent to see if it's a successful login page.
                        # print('html return ')#, p.text)

                        # TODO use this 'try except else' format everywhere
                        try:
                            # an authorised request.
                            # r = s.get(url, auth=(user,pswd), stream=True)
                            # r = s.get(url, auth=HTTPDigestAuth(user, pswd), stream=True)
                            r = s.get(str(url), cookies=cookies, stream=True)
                            # If the response was successful, no Exception will be raised
                            r.raise_for_status()
                        except HTTPError as http_err:
                            # https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
                            # raise HTTPError(f'HTTP error occurred: {http_err}')  # Python 3.6
                            _logger.exception(f"HTTP error occurred: {http_err}")
                            raise  #
                        except Exception as err:
                            # raise Exception(f'Other error occurred: {err}')  # Python 3.6
                            _logger.exception(f"Other error occurred: {err}")
                            raise  #
                        else:
                            # Success!
                            _logger.info(f"download completed, output on {fileout}")
                            # perc = float(i) / ?? * 100
                            # print(f'downloading file {uri} [{perc}%] on {fileout}', end='')
                            # print('Downloading File FooFile.txt [%d%%]\r'%i, end="")
                            with open(fileout, "wb") as f:
                                for chunk in r.iter_content(chunk_size=1024):
                                    if chunk:  # filter out keep-alive new chunks
                                        f.write(chunk)

        return d


if __name__ == "__main__":
    import doctest

    uri = "https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z"
    setupcfg.main()
    doctest.testmod(
        extraglobs={
            "t": DataObject(uri=uri),
            "datasetCsvPath": setupcfg.datasetCsvPath,
        },
        optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
    )


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
