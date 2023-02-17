import os
import configparser


def get_var(var_name):
    config = configparser.RawConfigParser()
    config.read('config.properties')

    return os.getenv(var_name, config.get('Properties', var_name))