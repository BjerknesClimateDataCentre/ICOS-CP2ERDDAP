#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# setupcfg.py

# ----------------------------------------------
# import from standard lib
from pathlib import Path
import logging
import logging.config
import yaml
import pkgutil
import sys
import os
import warnings
import argparse
import datetime as dt
from time import strftime, localtime
# import from other lib
import confuse  # Initialize config with your app
from dateutil.parser import parse
# import from my project
import icp2edd

# --- module's variable ------------------------
# public
global erddapPath, erddapWebInfDir, erddapContentDir, \
       datasetXmlPath, datasetCsvPath, \
       icp2eddPath, logPath, log_filename, \
       submFrom, submUntil, product, lastversion, \
       authorised_product, extraParam

# private
global _cfg_path, _update_log, _logcfg


def add_last_subm():
    """ register last submitted dates (used to load dataset)
    """
    global submUntil

    if submUntil is None:
        # use current date (UTC)
        submUntil = dt.datetime.now(dt.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()

    with open(_update_log, "a") as file:
        if _update_log.stat().st_size == 0:
            # add header to empty file
            file.write(f"# Previous submitted date(s) to load dataset from ICOS CP:\n")
        file.write(f"from {submFrom} until {submUntil}\n")


def _get_last_subm():
    """ read last ending submitted date (used to load dataset) registered
    """
    if _update_log.is_file() and _update_log.stat().st_size != 0:
        with open(_update_log, "rb") as file:
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR)
            return file.readline().decode().split('until')[1].rstrip('\n').lstrip()
    else:
        msg = f"Can not find file -{_update_log}- where look for last update"
        logging.debug(msg)
        raise FileNotFoundError(msg)


def _chk_product_subm_timeseries(dt_):
    """ check submitted date (used to load dataset) time series
    """
    # last update to be used
    duse = parse(dt_).isoformat()
    # last update registered
    try:
        dref = parse(_get_last_subm()).isoformat()
    except FileNotFoundError:
        # no previous date registered
        logging.info('No previous dates registered. Can not check time series')
    else:
        if dref < duse:
            logging.debug(f" last ending date registered -{dref}- lower than starting date to be used -{duse}-")
        elif dref > duse:
            logging.debug(f" last ending date registered -{dref}- greater than starting date to be used -{duse}-")


def _chk_product_subm(cfg_):
    """ check submitted dates

    dates assume to be UTC
    """
    global submFrom, submUntil

    try:
        _ = cfg_['product']['subm']['from'].get()
        if _ is not None:
            # submFrom = parse(_).astimezone(tz=dt.timezone.utc).isoformat()
            submFrom = parse(_).isoformat()
        else:
            submFrom = None
    except confuse.exceptions.NotFoundError:
        submFrom = None
    except Exception:
        logging.exception(f'Invalid date format (submitted from); '
                          f'Check arguments/configuration file(s)')
        raise  # Throw exception again so calling code knows it happened

    if submFrom is None:
        try:
            submFrom = _get_last_subm()
        except FileNotFoundError:
            # no previous date registered
            logging.warning('No previous dates registered. No initial date to your request.')
        except Exception:
            logging.exception(f'Something goes wrong when looking for last submitted date')
            raise  # Throw exception again so calling code knows it happened
    else:
        # check last update
        _chk_product_subm_timeseries(submFrom)

    try:
        _ = cfg_['product']['subm']['until'].get()
        if _ is not None:
            # submUntil = parse(_).astimezone(tz=dt.timezone.utc).isoformat()
            submUntil = parse(_).isoformat()
        else:
            submUntil = None
    except confuse.exceptions.NotFoundError:
        submUntil = None
    except Exception:
        logging.exception(f'Invalid date format (submitted until); '
                          f'Check arguments/configuration file(s)')
        raise  # Throw exception again so calling code knows it happened

    # check submission dates order
    if submFrom is not None and submUntil is not None and submFrom > submUntil:
        msg =  f"Invalid dates. " \
               f"End submission date -{submUntil}- lower than Start submission date -{submFrom}-. " \
               f"Check arguments/configuration file(s)"
        logging.exception(msg)
        raise ValueError(msg)


def _chk_config_product(cfg_):
    """ check submitted dates, product and version

    """
    global authorised_product, product
    global lastversion
    try:
        # check product submission
        _chk_product_subm(cfg_)

        # check product type
        try:
            product = cfg_['product']['type'].as_choice(authorised_product)
        except confuse.exceptions.NotFoundError:
            product = None
            # do not raise other exception as it will be by calling function

        # check product version
        try:
            lastversion = cfg_['product']['last'].get(bool)
        except confuse.exceptions.NotFoundError:
            lastversion = None
            # do not raise other exception as it will be by calling function

    except Exception:
        logging.exception("Something goes wrong when checking 'submission' parameters")
        raise  # Throw exception again so calling code knows it happened


def _search_file(cfg_, filename_):
    """ search file in several directory

    look for file 'filename_' in:
    - local directory or given path
    - user    config directory
    - package directory
    - package config directory

    :param cfg_:
    :param filename_: name of the file search
    :return: absolute path to filename_
    """
    global _cfg_path

    # check file exist
    if Path(filename_).is_file():
        # local directory
        return Path(filename_).absolute()
    elif Path(Path(cfg_.config_dir()) / filename_).is_file():
        # user config directory
        # ~/.config/<package> directory
        return Path(Path(cfg_.config_dir()) / filename_)
    elif Path(icp2eddPath / filename_).is_file():
        # ~/path/to/package/ directory
        return Path(icp2eddPath / filename_)
    elif Path(_cfg_path / filename_).is_file():
        # package config directory
        # ~/path/to/package/cfg directory
        return Path(_cfg_path / filename_)
    else:
        logging.exception(f"can not find file -{filename_}-; "
                          f'Check arguments/configuration file(s)')
        raise FileNotFoundError


def _chk_config_extra(cfg_):
    """
    """
    global extraParam

    try:
        extraParam = cfg_['extra']['parameters'].get(str)
    except confuse.exceptions.NotFoundError:
        logging.exception(f'Can not find extra parameters; '
                          f'Check arguments/configuration file(s)')
        raise  # Throw exception again so calling code knows it happened
    except Exception:
        logging.exception(f'Invalid parameters yaml filename; '
                          f'Check arguments/configuration file(s)')
        raise  # Throw exception again so calling code knows it happened

    # check config file exist
    extraParam = _search_file(cfg_, extraParam)


def _chk_config_authorised(cfg_):
    """
    """
    global authorised_product

    # Authorised product
    try:
        authorised_product = cfg_['authorised']['product'].get(list)
    except confuse.exceptions.NotFoundError:
        authorised_product = None
        # do not raise other exception as it will be by calling function


def _chk_config_log(cfg_):
    """
    """
    # see _setup_logger
    pass


def _chk_config_paths(cfg_):
    """
    """
    try:
        # check path to ERDDAP, and set up global variables
        #   path where ERDDAP has been previously installed, as well as
        #   path where xml files will be stored
        global erddapPath, erddapWebInfDir, erddapContentDir, datasetXmlPath

        erddapPath = Path(cfg_['paths']['erddap'].get(str))
        if not erddapPath.is_dir():
            raise FileNotFoundError('can not find ERDDAP path {}.\n'
                                    'Check config file(s) {} and/or {}'.format(erddapPath,
                                                                               cfg_.user_config_path(),
                                                                               cfg_.default_config_path))
        logging.debug(f'erddapPath: {erddapPath}')

        # erddapWebInfDir = erddapPath / 'webapps' / <ROOT> / 'WEB-INF'
        erddapWebInfDir = Path(cfg_['paths']['webinf'].get(str))
        if not erddapWebInfDir.is_dir():
            raise FileNotFoundError('can not find ERDDAP sub-directory {} \n'
                                    'check ERDDAP installation. '.format(erddapWebInfDir))
        logging.debug(f'erddapWebInfDir: {erddapWebInfDir}')

        erddapContentDir = erddapPath / 'content' / 'erddap'
        if not erddapContentDir.is_dir():
            raise FileNotFoundError('can not find ERDDAP sub-directory {} \n'
                                    'check ERDDAP installation'.format(erddapContentDir))
        logging.debug(f'erddapContentDir: {erddapContentDir}')

        datasetXmlPath = Path(cfg_['paths']['dataset']['xml'].as_filename())
        if not datasetXmlPath.is_dir():
            raise FileNotFoundError('can not find path where store dataset xml file {}.\n'
                                    'Check config file(s) {} and/or {}'.format(datasetXmlPath,
                                                                               cfg_.user_config_path(),
                                                                               cfg_.default_config_path))
        logging.debug(f'datasetXmlPath: {datasetXmlPath}')

        # check path to csv files, and set up global variable
        #   path where csv files will be stored
        global datasetCsvPath

        datasetCsvPath = Path(cfg_['paths']['dataset']['csv'].as_filename())
        if not datasetCsvPath.is_dir():
            raise FileNotFoundError('Can not find path where store dataset csv file {}.\n'
                                    'Check config file(s) {} and/or {}'.format(datasetCsvPath,
                                                                               cfg_.user_config_path(),
                                                                               cfg_.default_config_path))
        logging.debug(f'datasetCsvPath: {datasetCsvPath}')

        # check path to log files, and set up global variable
        #   path where log files will be stored
        global logPath

        logPath = Path(cfg_['paths']['log'].get(str))
        if not logPath.is_dir():
            logPath.mkdir(parents=True, exist_ok=True)
            warnings.warn('log path {} did not exist before.\n Check config file(s) {} and/or {}'.
                          format(logPath, cfg_.user_config_path(), cfg_.default_config_path))

        logging.debug(f'logPath: {logPath}')

    except Exception:
        logging.exception('Something goes wrong when checking paths')
        raise  # Throw exception again so calling code knows it happened


def _chk_config(cfg_):
    """
    :param cfg_: config from confuse _setup_config
    """
    try:
        # check paths parameters from configuration file(s)
        _chk_config_paths(cfg_)
        # check log parameters from configuration file(s)
        _chk_config_log(cfg_)
        # check authorised list from configuration file(s)
        _chk_config_authorised(cfg_)
        # check update parameters from configuration file(s)
        _chk_config_extra(cfg_)
        # check product parameters from configuration file(s)
        _chk_config_product(cfg_)
    except Exception:
        logging.exception('Something goes wrong when checking configuration file')
        raise  # Throw exception again so calling code knows it happened


def _find_package_path(name):
    # function from https://github.com/beetbox/confuse/blob/master/confuse/util.py
    """Returns the path to the package containing the named module or
    None if the path could not be identified (e.g., if
    ``name == "__main__"``).
    """
    # Based on get_root_path from Flask by Armin Ronacher.
    loader = pkgutil.get_loader(name)
    if loader is None or name == '__main__':
        return None

    if hasattr(loader, 'get_filename'):
        filepath = loader.get_filename(name)
    else:
        # Fall back to importing the specified module.
        __import__(name)
        filepath = sys.modules[name].__file__

    return os.path.dirname(os.path.abspath(filepath))


def _setup_logger(config_):
    """set up logger

    set up logging parameters from command line arguments
    otherwise from configuration file(s)
    otherwise from logging configuration file: /path/to/package/cfg/logging.yaml

    > Level and When it’s used
    > ------------------------
    > DEBUG:
    > Detailed information, typically of interest only when diagnosing problems.
    >
    > INFO:
    > Confirmation that things are working as expected.
    >
    > WARNING:
    > An indication that something unexpected happened, or indicative of some problem in the near
    > future (e.g. ‘disk space low’). The software is still working as expected.
    >
    > ERROR:
    > Due to a more serious problem, the software has not been able to perform some function.
    >
    > CRITICAL:
    > A serious error, indicating that the program itself may be unable to continue running.
    """
    global log_filename, _cfg_path, _logcfg

    _cfg_path = Path(_find_package_path(icp2edd.__pkg_cfg__))
    if not _cfg_path.is_dir():
        logging.exception('Can not find configuration path')
        raise FileNotFoundError

    _logcfg = _search_file(config_, 'logging.yaml')
    try:
        with open(_logcfg, 'rt') as file:
            cfg_log = yaml.safe_load(file.read())

            try:
                # overwrite default with config or parser value
                _log_level = config_['log']['level'].get(str)
                if _log_level is not None:
                    cfg_log['handlers']['console']['level'] = _log_level.upper()
            except confuse.exceptions.NotFoundError:
                pass
            except Exception:
                logging.exception(f'Invalid log level; '
                                  f'Check arguments/configuration file(s)')
                raise  # Throw exception again so calling code knows it happened

            try:
                # if verbose activated, print output on console
                _log_verbose = config_['log']['verbose'].get(bool)
                if _log_verbose is not None:
                    if not _log_verbose:
                        # disable log on console
                        cfg_log['handlers'].pop('console')
                        cfg_log['root']['handlers'].remove('console')
            except confuse.exceptions.NotFoundError:
                pass
            except Exception:
                logging.exception(f'Invalid log verbose; '
                                  f'Check arguments/configuration file(s)')
                raise  # Throw exception again so calling code knows it happened

            try:
                # rename log file with config or parser value
                _log_filename = config_['log']['filename'].get()
                if _log_filename is not None:
                    cfg_log['handlers']['file']['filename'] = _log_filename
            except confuse.exceptions.NotFoundError:
                pass
            except Exception:
                logging.exception(f'Invalid log filename; '
                                  f'Check arguments/configuration file(s)')
                raise  # Throw exception again so calling code knows it happened

            _paths_log = config_['paths']['log'].get()
            if _paths_log is not None:
                log_path = Path(str(_paths_log))
            else:
                # read path to output log file
                log_path = Path(cfg_log['handlers']['file']['filename']).parent

            if not log_path.is_dir():
                log_path.mkdir(parents=True, exist_ok=True)
                logging.warning(f'log path {log_path} did not exist before.\n Check config file(s) '
                                f'{config_.user_config_path()} and/or {config_.default_config_path}.')

            filename = cfg_log['handlers']['file']['filename']
            cfg_log['handlers']['file']['filename'] = str(log_path / filename)

            logging.config.dictConfig(cfg_log)
            # redirect warnings issued by the warnings module to the logging system.
            logging.captureWarnings(True)

            # keep log filename and path name
            log_filename = Path(cfg_log['handlers']['file']['filename']).resolve()

    except Exception:
        logging.exception('Error loading configuration file. Using default configs')
        raise  # Throw exception again so calling code knows it happened

    # add header to log file
    logging.info(f'-------------------')
    logging.info(f'package: {icp2edd.__name__}')
    logging.info(f'version: {icp2edd.__version__}')
    logging.info(f'start time: {strftime("%Y-%m-%d %H:%M:%S", localtime())}')
    logging.info(f'-------------------')


def _parse(logfile_):
    """set up parameter from command line arguments

    :param logfile_: log filename, useless except to change the default log filename when using checkOntology
    """
    # define parser
    parser = argparse.ArgumentParser(
        prog="icp2edd",
        description="blabla"
    )

    # positional arguments
    # parser.add_argument("name", type=str, help="file name")
    # optional arguments
    parser.add_argument("-v", "--verbose",
                        action="store_const",
                        const=True,
                        help="print status messages to stdout",
                        dest='log.verbose'
                        )
    parser.add_argument("--log_level",
                        type=str,
                        choices=['debug', 'info', 'warning', 'error', 'critical'],
                        help="stdout logger level",
                        dest='log.level'
                        )
    parser.add_argument("--log_filename",
                        type=str,
                        help="logger filename",
                        dest='log.filename'
                        )
    parser.add_argument("--log_path",
                        type=str,
                        help="logger path, where log will be stored",
                        dest='paths.log'
                        )
    parser.add_argument("--param",
                        type=str,
                        help="parameters configuration file",
                        dest='extra.parameters'
                        )
    parser.add_argument("--from",
                        type=str,
                        help="download dataset submitted from",
                        dest='product.subm.from'
                        )
    parser.add_argument("--until",
                        type=str,
                        help="download dataset submitted until",
                        dest='product.subm.until'
                        )
    parser.add_argument("--type",
                        type=str,
                        help="data 'type' to be used",
                        dest='product.type'
                        )
    parser.add_argument("--arguments",
                        action="store_const",
                        const=True,
                        help="print arguments value (from config file and/or inline argument) and exit",
                        dest='arguments'
                        )
    parser.add_argument("--version",
                        action="store_const",
                        const=True,
                        help="print release version and exit",
                        dest='version'
                        )

    # parse arguments
    args = parser.parse_args()

    if vars(args)['log.filename'] is None:
        vars(args)['log.filename'] = logfile_

    # TODO check and reformat args
    return args


def _setup_cfg():
    """set up from configuration file(s)

    read parameters from
    ~/.config/icp2edd/config.yaml
    otherwise from
    /path/to/package/cfg/config_default.yaml
    """
    # set up configuration file
    try:
        # Read configuration file
        config_ = confuse.LazyConfig('icp2edd', modname=icp2edd.__pkg_cfg__)  # Get a value from your YAML file

        # TODO check use of templates,
        #  cf examples in https://github.com/beetbox/confuse/tree/c244db70c6c2e92b001ce02951cf60e1c8793f75

        # set up default configuration file path
        pkg_path = Path(config_._package_path)
        config_.default_config_path = pkg_path / confuse.DEFAULT_FILENAME

        return config_

    except Exception:
        logging.exception("Something goes wrong when loading config file.")
        raise  # Throw exception again so calling code knows it happened


def _setup_path():
    """ set up some useful path
    """
    global icp2eddPath, _update_log

    icp2eddPath = Path(_find_package_path(__package__))
    if not icp2eddPath.is_dir():
        logging.exception('Can not find package path')
        raise FileNotFoundError

    update_log_path = icp2eddPath / '.log'
    if not update_log_path.is_dir():
        update_log_path.mkdir(parents=True, exist_ok=True)
        logging.warning(f'update log path -{update_log_path}- did not exist before.')

    _update_log = update_log_path / 'update.log'


def _default_logger():
    """creates default logger, before any setting up

    this default logger should only be used in case of any exception raised during setting up
    """
    logging.basicConfig(
        level=logging.INFO,
        style='{',
        format="{asctime} | {levelname:8} | {name} | {message}"
    )
    # redirect warnings issued by the warnings module to the logging system.
    logging.captureWarnings(True)


def _show_arguments(cfg_, print_=False):
    """ """
    logging.debug(f"config files:")
    logging.debug(f"   pkg              : {cfg_.default_config_path}")
    logging.debug(f"   user             : {cfg_.user_config_path()}")
    logging.debug(f"   logging          : {_logcfg}")
    logging.debug(f"   update           : {_update_log}\n")

    logging.debug(f"paths.erddap        : {erddapPath}")
    logging.debug(f"paths.webinf        : {erddapWebInfDir}")
    logging.debug(f"paths.dataset.csv   : {datasetCsvPath}")
    logging.debug(f"paths.dataset.xml   : {datasetXmlPath}")
    logging.debug(f"paths.log           : {logPath}\n")

    logging.debug(f"log.filename        : {log_filename} ")
    logging.debug(f"log.verbose         : {cfg_['log']['verbose']}  ")
    logging.debug(f"log.level           : {cfg_['log']['level']}\n")

    logging.debug(f"authorised.product  : {authorised_product}\n")

    logging.debug(f"extra.parameters    : {extraParam}\n")

    logging.debug(f"product.sub.from    : {submFrom}")
    logging.debug(f"product.sub.until   : {submUntil}")
    logging.debug(f"product.type        : {product}")
    logging.debug(f"product.last        : {lastversion}")

    if print_:
        print(f"config files:")
        print(f"   pkg              : {cfg_.default_config_path}")
        print(f"   user             : {cfg_.user_config_path()}")
        print(f"   logging          : {_logcfg}")
        print(f"   update           : {_update_log}\n")

        print(f"paths.erddap        : {erddapPath}")
        print(f"paths.webinf        : {erddapWebInfDir}")
        print(f"paths.dataset.csv   : {datasetCsvPath}")
        print(f"paths.dataset.xml   : {datasetXmlPath}")
        print(f"paths.log           : {logPath}\n")

        print(f"log.filename        : {log_filename} ")
        print(f"log.verbose         : {cfg_['log']['verbose']}  ")
        print(f"log.level           : {cfg_['log']['level']}\n")

        print(f"authorised.product  : {authorised_product}\n")

        print(f"extra.parameters    : {extraParam}\n")

        print(f"product.sub.from    : {submFrom}")
        print(f"product.sub.until   : {submUntil}")
        print(f"product.type        : {product}")
        print(f"product.last        : {lastversion}")
        exit(0)


def _show_version():
    """ """
    # print release version
    print(f'package: {icp2edd.__name__}')
    print(f'version: {icp2edd.__version__}')
    exit(0)


def main(logfile_=None):
    """set up icp2edd

    set up config file(s)
    set up logger

    :param logfile_: log filename, useless except to change the default log filename when using checkOntology
    """

    # init default
    _default_logger()

    # setup package path
    _setup_path()

    # read configuration file(s)
    config = _setup_cfg()

    # read command line arguments
    args = _parse(logfile_)

    if args.version:
        _show_version()

    # overwrite configuration file parameter with parser arguments
    config.set_args(args, dots=True)

    # read logging configuration file
    _setup_logger(config)

    # check configuration file
    _chk_config(config)

    # print parameters use from config file and/or inline command
    _show_arguments(config, args.arguments)


if __name__ == '__main__':
    main()

    _logger = logging.getLogger(__name__)
    _logger.debug('This message should go to the log file')
    _logger.info('So should this')
    _logger.warning('And this, too')
    _logger.error('\tAnd non-ASCII stuff, too, like Øresund and Malmö\n')
    _logger.critical('this is critical')
    # _logger.exception('raise en exception')
