#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __main__.py

# ----------------------------------------------
# import from standard lib
import logging
from pathlib import Path

# import from other lib
# import from my project
import icp2edd.csv4Erddap as c4edd
import icp2edd.parameters as parameters
import icp2edd.setupcfg as setupcfg
import icp2edd.timing
import icp2edd.xml4Erddap as x4edd
from icp2edd.icpobj import *  # see icpobj/__init__.py
from icp2edd.superIcpObj import SuperICPObj


# ----------------------------------------------
def main():
    """ """
    print(f"Running {__file__} \n...")

    # set up logger, paths, ...
    setupcfg.main()
    _logger = logging.getLogger(__name__)

    # check parameters file
    param = parameters.main()

    # First part get new dataObject on ICOS CP, and create associated ERDDAP dataset.xml
    _logger.info(
        "-1- get new dataObject on ICOS CP, and create associated ERDDAP dataset.xml\n"
    )

    _logger.info("get DataObject metadata from ICOS CP")
    try:
        # uri = 'https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z'
        # dataobjs = DataObject(uri=uri)
        dataobjs = cpmeta.DataObject(
            submfrom=setupcfg.submFrom,
            submuntil=setupcfg.submUntil,
            product=setupcfg.product,
            lastversion=setupcfg.lastversion,
        )
    except Exception:
        _logger.exception("Something goes wrong when setting up DataObject")
        raise  # Throw exception again so calling code knows it happened

    _logger.info("read DataObject from ICOS-CP:")
    try:
        dataobjs.getMeta()
    except Exception:
        _logger.exception("Something goes wrong when loading DataObj metadata")
        raise  # Throw exception again so calling code knows it happened

    _logger.info("download DataObject from ICOS-CP")
    try:
        dd = dataobjs.download()
    except Exception:
        _logger.exception("Something goes wrong when downloading DataObject data")
        raise  # Throw exception again so calling code knows it happened

    # loop on each dataset downloaded
    for csv, dict in dd.items():

        rep = dict["path"]
        doi = dict["doi"]

        _logger.info(
            "change in csv file :\n\t\t- change Date/Time format\n\t\t- remove units for variable name"
        )
        try:
            fileout = Path.joinpath(rep, csv)
            c4edd.modify(fileout, doi)
        except Exception:
            _logger.exception("Something goes wrong when modifying csv file")
            raise  # Throw exception again so calling code knows it happened

        _logger.info("run ERDDAP GenerateDatasetXml tool to create dataset.xml file")
        try:
            dirout = fileout.parents[1]
            xml = x4edd.Xml4Erddap(dirout)
        except Exception:
            _logger.exception(
                "Something goes wrong when initialising Xml2ERDDAP object"
            )
            raise  # Throw exception again so calling code knows it happened

        # run GenerateDatasetXml
        try:
            xml.generate()
        except Exception:
            _logger.exception(
                "Something goes wrong when generating ERDDAP dataset.xml file"
            )
            raise  # Throw exception again so calling code knows it happened

    _logger.info("concatenate every dataset file(s) into one")
    # concatenate header.xml dataset.XXX.xml footer.xml into local datasets.xml
    dsxmlout = x4edd.concatenate()

    # Second part get ICOS CP metadata up to date, and update ERDDAP datasets.xml
    _logger.info(
        "-2- get ICOS CP metadata up to date, and update ERDDAP datasets.xml\n"
    )
    _logger.info(
        "change/add metadata on datasets.xml file, considering metadata from ICOS CP"
    )

    # TODO what about metadata add directly/manually in older dataset.xml ??
    #   - keep release of former dataset.xml file
    #   - check attributes diff with new dataset.xml
    #   - get and push unique attributes from former dataset.xml in new one

    # get all metadata from dataObject use by ERDDAP
    try:
        _logger.info(f"initialise SuperICPObj object")
        superObj = SuperICPObj()
        gloatt = superObj.getAttr()
        superObj.show()

    except Exception:
        _logger.exception("Something goes wrong when initialising SuperICPObj")
        raise  # Throw exception again so calling code knows it happened

    try:
        _logger.info("change/add attributes into local datasets.xml")
        x4edd.changeAttr(dsxmlout, gloatt)
        _logger.info("replace ERDDAP datasets.xml file with the new one")
        x4edd.replaceXmlBy(dsxmlout)

    except Exception:
        _logger.exception(
            "Something goes wrong when changing/adding attributes into ERDDAP datasets.xml"
        )
        raise  # Throw exception again so calling code knows it happened

    # store ending submitted date of current update
    setupcfg.add_last_subm()


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("Something goes wrong!!!")
        raise  # Throw exception again so calling code knows it happened

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
