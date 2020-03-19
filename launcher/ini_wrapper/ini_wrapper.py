import configparser
import os

import logging
import ini_wrapper


class IniWrapper:

    def __init__(self,
                 file_name
                 ):
        self.logger = logging.getLogger(ini_wrapper.LOGGER_NAME)
        self.data = dict()
        self.file_name = file_name
        if os.path.isfile(file_name):
            self.config = configparser.ConfigParser()
            self.config.read(self.file_name)
        else:
            self.config = None
        self.logger.debug('Create: {}'.format(repr(self)))

    def read_data(self):
        """ Modify to load data for specific application """
        """ 
        if self.config and self.config['SECTION']['my_ini_var']:
            set_value = self.config['MAIN']['my_ini_var'].replace('"', '')
            self.data['my_ini_var'] = set_value
        else:
            self.data['my_ini_var'] = 'default value'
        """
        if self.config and self.config['MAIN']['ApiUrl']:
            set_value = self.config['MAIN']['ApiUrl'].replace('"', '')
            self.data['ApiUrl'] = set_value
        else:
            self.data['ApiUrl'] = 'http://httpbin.org/post'

        if self.config and self.config['MAIN']['CronCommand']:
            set_value = self.config['MAIN']['CronCommand'].replace('"', '')
            self.data['CronCommand'] = set_value
        else:
            self.data['CronCommand'] = 'python3 main.py'

        if self.config and \
                ('MAIN' in self.config) and \
                ('CronId' in self.config['MAIN']):
            set_value = self.config['MAIN']['CronId'].replace('"', '')
            self.data['CronId'] = set_value
        else:
            self.data['CronId'] = 'periodic-launcher'

        self.logger.debug('Set data: {}'.format(self.data))

    def __repr__(self):
        return "IniWrapper('{}')"\
            .format(self.file_name)

    def __str__(self):
        return self.file_name

