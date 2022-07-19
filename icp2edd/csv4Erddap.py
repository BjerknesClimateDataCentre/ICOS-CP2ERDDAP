#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# csv4Erddap.py

# --- import -----------------------------------
# import from standard lib
import logging
from pathlib import Path

# import from other lib
# > conda forge
import pandas as pd
from dateutil.parser import parse

# import from my project
import icp2edd.util as util

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)


# ----------------------------------------------
def time_format(datetime_, pre_=3):
    """
    change date/time format from whatever to iso 8601 with only 'pre_' decimal

    :param datetime_: input date and time
    :param pre_: precision (number of decimal)

    :return:  date/time (format: iso 8601 with 'pre_' decimal)

    >>> tt = '2019-07-11T10:55:52.000000Z'
    >>> time_format(tt)
    '2019-07-11T10:55:52.000Z'
    >>> tt = '23/12/99'
    >>> time_format(tt, 4)
    '1999-12-23T00:00:00.0000Z'
    """
    if not isinstance(datetime_, str):
        raise TypeError(f"Invalid type value, datetime {datetime_} must be string.")

    if not isinstance(pre_, int):
        raise TypeError(f"Invalid type value, precision {pre_} must be integer.")

    try:
        dt = parse(datetime_)
    except Exception:
        _logger.exception(f"Something goes wrong when parsing -{datetime_}-")
        raise  #

    cc = 10 ** (6 - pre_)
    pre_ = str(pre_)

    fmt1 = "%s.%0" + str(pre_) + "i%s"
    fmt2 = "%" + str(pre_) + "i"

    return fmt1 % (
        dt.strftime("%Y-%m-%dT%H:%M:%S"),
        float(fmt2 % (round(dt.microsecond / cc))),
        dt.strftime("Z"),
    )


def modify(f, doi_=None):
    """
    overwrite csv file 'f' after few change:
    - remove units from variable name
    - reformat Date/Time with 3 decimals
    - add a column with 'doi'

    :param f: csv file to be changed

    TODO check output file, see unittest and mock file
    """
    if not isinstance(f, Path):
        raise TypeError(f"Invalid type value, f -{f}- must be Path object")

    # Read data from file 'filename.csv'
    data = pd.read_csv(f)

    # remove units from variable name
    # WARNING: report change on header on superObj.DatasetVariable keys
    # TODO see how ERDDAP handle second line with unit, and unit between parentheses ?
    # data.rename(columns=lambda x: re.sub(r'(.*)(\[.*\])(.*)', r'\1'r'\3', x), inplace=True)
    data.rename(columns=lambda x: util.filterBracket(x), inplace=True)

    # reformat Date & Time with 3 decimals only
    dt_list = ["Date/Time", "TIMESTAMP"]  # column name
    if any(dt in data for dt in dt_list):
        for dt in dt_list:
            if dt in data:
                data[dt] = data[dt].apply(lambda x: time_format(x, 3))
    else:
        _logger.warning(f"Can not find 'Date/Time' column in csv file -{f}-")

    # add 'doi' column
    data["doi"] = doi_

    # Preview the first 5 lines of the loaded data
    # print(data.head())

    # Warning : overwrite file
    data.to_csv(f, date_format="%Y-%m-%dT%H:%M:%S.%fZ", index=False)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

    # csvDir = Path('/home/jpa029/Data/ICOS2ERDDAP/58GS20190711_SOCAT_enhanced')
    # csv = csvDir / '58GS20190711_SOCAT_enhanced.csv.bak'
    # modify(csv)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
