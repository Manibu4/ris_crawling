"""
Module to run the application.
"""

#import logging, logging.config, yaml
#logging.config.dictConfig(yaml.load(open('stiftung/settings/logging.conf')))
from ris_crawling.run import blu

blu.run(host='0.0.0.0', port=1234)
