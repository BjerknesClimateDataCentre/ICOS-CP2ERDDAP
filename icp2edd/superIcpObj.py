#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# superIcpObj.py

"""
    This module set up a generic class for super ICOS CP Object.

    Example usage:

    from superIcpObj import SuperICPObj

    supericpobj = SuperICPObj()     # initialise SuperICPObj
    supericpobj.getMeta()           # get metadata from ICOS CP
    supericpobj.show()              # print metadata
"""

# --- import -----------------------------------
# import from standard lib
import logging
import traceback
from pathlib import Path
from pprint import pformat

# import from other lib
from SPARQLWrapper.SmartWrapper import Value as SmartWrapperValue

# > conda-forge
# import from my project
import icp2edd.parameters as parameters
import icp2edd.setupcfg as setupcfg
import icp2edd.util as util
from icp2edd.icpobj import *

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)

list_VariableObject = ["cpmeta.DatasetVariable", "cpmeta.DatasetColumn"]
list_DataObject = ["cpmeta.DataObject"]

# list of object to not dig in to avoid infinity loop / recursive search
list_rec_search = ["NextVersionOf", "RevisionOf", "PrimarySource", "QualityFlagFor"]

# ----------------------------------------------
class SuperICPObj(object):
    """ """

    def __init__(
        self,
        submfrom=None,
        product=None,
    ):
        """Initialise generic SuperICPObj.

        It will be used to set up a sparql query, and get all metadata of ICPObj from ICOS CP.

        Optionally we could select DataObject:
            - submitted from date 'submfrom'
            - submitted from product 'product'
        """
        self._from = submfrom
        self._product = product
        #
        self.meta = {}
        self.DataObject = {}
        self.DataVariable = {}
        self.classprop = {}
        #
        self.tmp = {}

        # check parameters file
        param = parameters.main()
        #
        self.dict_convAttr = param["attributes"]["convert"]

        try:
            if self._from is None:
                # to avoid too large Request-URI, loop over listuri
                # list uri of all datasets already loaded
                listuri = self._listDatasetLoaded()
                # listuri = ["https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z",]
                # listuri = ["https://meta.icos-cp.eu/objects/-GpJLAEmZzHt48iB3l1eBuct"]
                for uri in listuri:
                    _logger.info("get DataObject metadata from ICOS CP")
                    _ = cpmeta.DataObject(uri=uri)
                    _.getMeta()
                    _.show()
                    #
                    self.meta = {**_.meta, **self.meta}
            else:
                # list all datasets submitted since self._from
                _logger.info(
                    f"get DataObject metadata from ICOS CP submitted since {self._from}"
                )
                # uri = "https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z"
                # _ = cpmeta.DataObject(uri=uri)
                _ = cpmeta.DataObject(submfrom=self._from, product=self._product)
                _.getMeta()
                _.show()
                #
                self.meta = {**_.meta, **self.meta}

        except Exception:
            _logger.exception(
                "Something goes wrong when loading metadata from DataObject"
            )
            raise  # Throw exception again so calling code knows it happened

        # get instance name
        (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
        self._instance_name = text[: text.find("=")].strip()

    def getAttr(self):
        """ """
        list_dataObj = list(self.meta.keys())
        # fill self.meta
        for uri in list_dataObj:
            print(f"\nlook in uri: {uri} ", end="")
            _logger.info(f"look in uri: {uri}")
            self._getSubAttr(uri)
        print(f"")

        # ll=['http://meta.icos-cp.eu/resources/cpmeta/temperature','http://meta.icos-cp.eu/resources/cpmeta/portion','http://meta.icos-cp.eu/resources/cpmeta/salinity']
        # self.repackMeta(self.meta.keys())
        # print(pformat(self.tmp))

        # repack with objtype
        for uri in list_dataObj:
            # get object type
            print(f"\nspread in uri: {uri} ", end="")
            self.repack(uri)
        print(f"")

        return {**self.DataObject, **self.DataVariable}

    def _renameKeyDic(self, _):
        """
        rename dictionary keys (if listed in dict_convAttr):
        :return: renamed dictionary
        """
        for oldKey, newKey in self.dict_convAttr.items():
            _ = dict((newKey, v) if k == oldKey else (k, v) for k, v in _.items())
        return _

    def repack(self, uri_):
        # TODO see if it could be merge with getSubAttr
        _logger.debug(f"repack uri {uri_}")

        def spread(uri_, exclude_=[], cnt_=0):

            cnt_ += 1
            print("." * cnt_, end="", flush=True)

            self.tmp[uri_] = {}
            if uri_ not in self.meta.keys():
                _logger.critical(f"Try spreading unknown uri -{uri_}-")
                raise SystemExit(1)

            for k, lv in self.meta[uri_].items():
                if k in ["uri"]:
                    _logger.debug(f"ignore uri attribute")
                    # if k not in self.tmp[uri_].keys():
                    #     d = {k: str(lv[0].value)}
                    #     self.tmp[uri_] = util.combine_dict_in_list(d, self.tmp[uri_])
                elif k in list_rec_search:
                    _logger.debug(
                        f"ignore {k} attribute. do not iterate to avoid recursive search"
                    )
                else:
                    for v in lv:
                        if not isinstance(v, SmartWrapperValue):
                            raise TypeError(
                                "invalid type: element -{v}- must be of type SmartWrapperValue"
                            )

                        d = {}
                        if v.type != "uri":
                            d[k] = [v.value]
                        else:
                            objtype = ICPObj(uri=v.value).objtype
                            if objtype not in exclude_:
                                if v.value in self.tmp.keys():
                                    for kk, vv in self.tmp[v.value].items():
                                        # separator between object and attribute
                                        kkk = k + _sep + kk
                                        d[kkk] = vv
                                else:
                                    dd = spread(v.value, exclude_=exclude_, cnt_=cnt_)
                                    for kk, vv in dd.items():
                                        # separator between object and attribute
                                        kkk = k + _sep + kk
                                        d[kkk] = vv
                            else:
                                self.repack(v.value)

                        d = self._renameKeyDic(d)
                        self.tmp[uri_] = util.combine_dict_in_list(d, self.tmp[uri_])

            return self.tmp[uri_]

        # check object type
        _ = ICPObj(uri=uri_)
        objtype = _.objtype

        if objtype in list_DataObject:
            # Warning: linked to:
            # - 'cpmeta:hasName' in StaticObject
            if "filename" not in self.meta[uri_]:
                _logger.critical(
                    f"can not find 'filename' attribute in meta of {uri_}.\n "
                    f"Check value of 'cpmeta:hasName' in StaticObject"
                )
            filename = Path(self.meta[uri_]["filename"][0].value)
            # datasetId = case.camel('icos_' + filename.stem, sep='_')
            datasetId = util.datasetidCase(filename)

            self.DataObject[datasetId] = spread(uri_, exclude_=list_VariableObject)

        elif objtype in list_VariableObject:
            # Warning: linked to:
            # - 'cpmeta:hasColumnTitle in DatasetColumn
            if "column_title" not in self.meta[uri_]:
                _logger.critical(
                    f"can not find 'column_title' attribute in meta of {uri_}.\n "
                    f"Check value of 'cpmeta:hasColumnTitle' in DatasetColumn"
                )
            varname = self.meta[uri_]["column_title"][0].value
            # variableId = case.camel(varname, sep='_')
            variableId = util.filterBracket(varname)

            self.DataVariable[variableId] = spread(uri_)

        else:
            _logger.error(f"should not be run objtype {objtype}")

        # clean
        # self.tmp = {}

    def _getSubAttr(self, uri_, cnt_=0):
        """
        dict1 = {name: value, name: value, ...}

        special cases for keys 'uri' and 'NextVersionOf'.
        - 'uri': do not iterate to avoid infinity loop
        - 'NextVersionOf' : do not iterate to avoid recursive search inside previous versions
        """
        cnt_ += 1
        print("." * cnt_, end="", flush=True)

        for k, lv in self.meta[uri_].items():
            if k == "uri":
                # do nothing, you are currently exploring it
                _logger.debug(f"do nothing, you are currently exploring this uri -{k}-")
            elif k in list_rec_search:
                # Warning: linked to:
                # - 'cpmeta:isNextVersionOf'  in StaticObject, and Collection
                # - 'cpmeta:isQualityFlagFor' in DatasetColumn
                # - 'prov:hadPrimarySource'   in StaticObject, and Collection
                # - 'prov:wasRevisionOf'      in StaticObject, and Collection
                _logger.debug(
                    f"key {k} found. do not iterate to avoid recursive search"
                )
            else:
                for v in lv:
                    if not isinstance(v, SmartWrapperValue):
                        raise TypeError(
                            "invalid type: element -{v}- must be of type SmartWrapperValue"
                        )

                    if v.type == "uri":
                        uri = v.value
                        if uri in self.meta:
                            _logger.debug(f"do nothing, uri -{uri}- already in meta")
                        else:
                            # check object type
                            _ = ICPObj(uri=uri)
                            objtype = _.objtype

                            # dummy patch cause issue on instrument data
                            # https://meta.icos-cp.eu/objects/Rd3xqDBV1PhqO-7Y9GGIRw0q
                            if objtype is not None:
                                try:
                                    klass = type(globals()[objtype]())
                                    _ = klass(uri=uri)
                                    try:
                                        _.getMeta()
                                        self.meta = {**_.meta, **self.meta}
                                        _logger.debug(
                                            f"dig into to explore {objtype} uri: {uri}"
                                        )
                                        self._getSubAttr(uri, cnt_)
                                    except Exception:
                                        _logger.exception(
                                            f"can not found metadata from {objtype}[{uri}]"
                                        )
                                        raise
                                except Exception:
                                    _logger.exception(
                                        f"can not found class {objtype}, for object {uri}"
                                    )
                                    raise
                            else:
                                self.meta[uri] = {}

    def _listDatasetLoaded(self):
        """ """
        # list directory containing csv file, return directory name
        output = set()
        for csv in setupcfg.datasetCsvPath.glob("**/*.csv"):
            output.add(csv.parent.name + ".csv")

        # list URI related to those directory name(s)
        uri_list = []
        for chunk in util.chunks(list(output), 10):
            _ = cpmeta.DataObject()
            uri_list.append(_.listUri(list(chunk)))

        return uri_list

    def show(self, print_=False):
        """ """
        if not isinstance(print_, bool):
            _logger.error(f"Invalid type argument -{print_}-")
            raise TypeError("Invalid type argument")

        _logger.info(f"Class name: SuperICPObj:\n {pformat(self.meta)}")
        if print_:
            print("\nClass name: SuperICPObj")
            print("\t" + pformat(self.meta))

        _logger.info(f"DataObject dictionary:\n {pformat(self.DataObject)}")
        if print_:
            # Check if dictionary is empty
            empty = not bool(self.DataObject)
            print("\nDataObject dictionary:")
            if not empty:
                print(f"\t{pformat(self.DataObject)}")
            else:
                print(f"\tself.DataObject dictionary empty !")

        _logger.info(f"DataVariable dictionary:\n {pformat(self.DataVariable)}")
        if print_:
            # Check if dictionary is empty
            empty = not bool(self.DataVariable)
            print("\nDataVariable dictionary:")
            if not empty:
                print(f"\t{pformat(self.DataVariable)}")
            else:
                print(f"\tself.DataVariable dictionary empty !")

    def getClassProperties(self):
        """ """
        list_dataObj = self.meta.keys()
        # fill self.meta
        for uri in list_dataObj:
            print(f"\nlook in uri: {uri} ", end="")
            _logger.info(f"look in uri: {uri}")
            self._getSubAttr(uri)
        print(f"")

        # get properties for each class object
        for uri in self.meta.keys():
            print(f"\nlook for properties in uri: {uri} ", end="")
            _logger.info(f"look for properties in uri: {uri}")
            _ = ICPObj(uri=uri)
            objtype = _.objtype.replace(".", ":")
            if objtype not in self.classprop:
                self.classprop[objtype] = set()
            list_props = _.getProperties()
            # add properties if not already listed
            self.classprop[objtype] = {*list_props, *self.classprop[objtype]}

    def _getSubProp(self, uri_, cnt_=0):
        """
        dict1 = {name: value, name: value, ...}

        special cases for keys 'uri' and 'NextVersionOf'.
        - 'uri': do not iterate to avoid infinity loop
        - 'NextVersionOf' : do not iterate to avoid recursive search inside previous versions
        """
        cnt_ += 1
        print("." * cnt_, end="", flush=True)

        for k, lv in self.meta[uri_].items():
            if k == "uri":
                # do nothing, you are currently exploring it
                _logger.debug(f"do nothing, you are currently exploring this uri -{k}-")
            elif k in list_rec_search:
                # Warning: linked to:
                # - 'cpmeta:isNextVersionOf' in StaticObject, and Collection
                # - 'cpmeta:isQualityFlagFor' in DatasetColumn
                # - 'prov:hadPrimarySource'  in StaticObject, and Collection
                # - 'prov:wasRevisionOf'     in StaticObject, and Collection
                _logger.debug(
                    f"key {k} found. do not iterate to avoid recursive search"
                )
            else:
                for v in lv:
                    if not isinstance(v, SmartWrapperValue):
                        raise TypeError(
                            "invalid type: element -{v}- must be of type SmartWrapperValue"
                        )

                    if v.type == "uri":
                        uri = v.value
                        if uri in self.meta:
                            _logger.debug(f"do nothing, uri -{uri}- already in meta")
                        else:
                            # check object type
                            _ = ICPObj(uri=uri)
                            objtype = _.objtype

                            try:
                                klass = type(globals()[objtype]())
                                _ = klass(uri=uri)
                                try:
                                    _.getMeta()
                                    self.meta = {**_.meta, **self.meta}
                                    _logger.debug(
                                        f"dig into to explore {objtype} uri: {uri}"
                                    )
                                    self._getSubAttr(uri, cnt_)
                                except Exception:
                                    _logger.exception(
                                        f"can not found metadata from {objtype}[{uri}]"
                                    )
                                    raise
                            except Exception:
                                _logger.exception(f"can not found class {objtype}")
                                raise


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
