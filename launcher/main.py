import logging
import logger_wrapper
import argparse
import os
from datetime import datetime

from json_wrapper.json_wrapper import JsonWrapper
from api_wrapper.api_wrapper import ApiWrapper
from ini_wrapper.ini_wrapper import IniWrapper
from logger_wrapper.logger_wrapper import LoggerWrapper
from cron_wrapper.cron_wrapper import CronWrapper

in_args = argparse.ArgumentParser()
in_args.add_argument('-i', '--install', help='Install/update cron table')
in_args.add_argument('-u', '--uninstall', help='Delete cron table', action='store_true')
in_args.add_argument('-c', '--config', type=str,  help='Set alternative *ini file')
in_args.add_argument('-t', '--crontab', help='List configured cron table', action='store_true')
in_args.add_argument('-v', '--verbose', help='Verbose output', action='store_true')
in_args.add_argument('-ll', '--log_level', help='Set log level for this run.',
                     choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])
in_args.add_argument('-s', '--api_send', help='Send start command with send date time (yyyy-mm-dd hh:mm:ss)')
akt_args = in_args.parse_args()

lw = LoggerWrapper()
logger_name = logger_wrapper.LOGGER_NAME
logger = logging.getLogger(logger_name)
if akt_args.log_level:
    logger = lw.set_logger(logger, akt_args.verbose, akt_args.log_level)
elif akt_args.verbose:
    logger = lw.set_logger(logger, akt_args.verbose)
else:
    logger = lw.set_logger(logger)


def send(par_dt_str = None):
    logger.info("--------- Send starter ----------")
    if akt_args.config:
        str_config = akt_args.config
    else:
        str_config = 'main.ini'
    ini_obj = IniWrapper(str_config)
    ini_obj.read_data()
    json_obj = JsonWrapper.from_none()
    if par_dt_str is None:
        now = datetime.now()
        str_now = now.strftime("%Y-%m-%d %H:%M:%S")
    else:
        str_now = par_dt_str
    logger.info("reference date = {}".format(str_now))
    json_obj.dict = dict()
    json_obj.dict['start'] = str_now
    a_w = ApiWrapper(ini_obj.data['ApiUrl'])
    logger.info("send to api: {}".format(ini_obj.data['ApiUrl']))
    a_w.post_json(json_obj.get_json())
    logger.info('--------- END ----------')
    return


def install():
    logger.info("--------- Install cron ----------")
    if akt_args.config:
        str_config = akt_args.config
    else:
        str_config = 'main.ini'
    if not os.path.isfile(str_config):
        logger.error("Can't find config file {}".format(str_config))
        raise Exception("Can't find config file {}".format(str_config))
    ini_obj = IniWrapper(str_config)
    ini_obj.read_data()

    cron = CronWrapper(akt_args.install, ini_obj.data['CronCommand'])
    cron.install()

    logger.info('--------- END ----------')
    return


def list_cron():
    logger.info("--------- List cron ----------")
    if akt_args.config:
        str_config = akt_args.config
    else:
        str_config = 'main.ini'
    if not os.path.isfile(str_config):
        logger.error("Can't find config file {}".format(str_config))
        raise Exception("Can't find config file {}".format(str_config))
    ini_obj = IniWrapper(str_config)
    ini_obj.read_data()

    cron = CronWrapper(None, ini_obj.data['CronCommand'])
    file_content = cron.crontab_list
    print("List of existing cron commands:")
    for line in file_content:
        if not line.startswith("#"):
            if not line.startswith("\n"):
                print(line)
    logger.info('--------- END ----------')
    return


def uninstall_cron():
    logger.info("--------- Uninstall cron ----------")
    if akt_args.config:
        str_config = akt_args.config
    else:
        str_config = 'main.ini'
    if not os.path.isfile(str_config):
        logger.error("Can't find config file {}".format(str_config))
        raise Exception("Can't find config file {}".format(str_config))
    ini_obj = IniWrapper(str_config)
    ini_obj.read_data()

    cron = CronWrapper(None, ini_obj.data['CronCommand'])
    cron.uninstall_cron()

    logger.info('--------- END ----------')
    return


def main():
    if akt_args.install:
        install()
    elif akt_args.crontab:
        list_cron()
    elif akt_args.uninstall:
        uninstall_cron()
    elif akt_args.api_send:
        send(akt_args.api_send)
    else:
        send()
    return


if __name__ == '__main__':
    main()
