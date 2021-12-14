#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ecosystemType.py

"""
    The ecosystemType module is used to explore ICOS CP cpmeta::EcosystemTypes' metadata.

    Example usage:

    from cpmeta import EcosystemType

    ecosystemTypes = EcosystemType()     # initialise ICOS CP EcosystemType object
    ecosystemTypes.get_meta()            # get ecosystemTypes' metadata from ICOS CP
    ecosystemTypes.show()                # print ecosystemTypes' metadata
"""

# --- import -----------------------------------
# import from standard lib
import logging
import traceback

# import from other lib
# import from my project
from icp2edd.icpobj import ICPObj

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)

# object attributes' dictionary with RDF 'property' as key and RDF 'object' as value
#   RDF triples: 'subject' + 'property/predicate' + 'object/value'
# {'property/predicate': 'object/value'}
# Note: 'object/value' will be the output attribute name
_attr = {
    "skos:broader": "broader",  #
    # subproperty {
    # "cpmeta:broaderEcosystem": "broader_ecosystem",  # cpmeta/EcosystemType
    # }
}
# list of equivalent class
_equivalentClass = []

# cpmeta/Site       is subClassOf cpmeta/EcosystemType

# ----------------------------------------------
class EcosystemType(ICPObj):
    """
    >>> t.getMeta()
    >>> t.show(True)

    """

    def __init__(self, limit=None, uri=None):
        """initialise instance of EcosystemType(ICPObj).

        It will be used to set up a sparql query, and get all metadata of EcosystemType from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select EcosystemType:
        - with ICOS CP 'uri'

        Example:
            EcosystemType(limit=5)

        :param limit: number of returned results
        :param uri: ICOS CP URI ('https://meta.fieldsites.se/resources/ecosystems/water-course')
        """
        super().__init__()
        # set up class/instance variables
        self._uri = uri
        self._limit = limit

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
        self._object = "http://meta.icos-cp.eu/ontologies/cpmeta/EcosystemType"

        #
        self._objtype = None
        if self._object is not None:
            self.objtype = self._getObjectType()

        # get instance name
        (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
        self._instance_name = text[: text.find("=")].strip()


if __name__ == "__main__":
    import doctest

    doctest.testmod(
        extraglobs={"t": EcosystemType(limit=10)},
        optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
    )


# See PyCharm help at https://www.jetbrains.com/help/pycharm/