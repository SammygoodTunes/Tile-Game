
"""
Logger for logging debug info, warnings and errors.
"""

import argparse
import logging
from os import path, mkdir
from sys import stdout
from time import strftime

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action=argparse.BooleanOptionalAction,
                    default=False, type=bool, help='enable debug info')
args, unknown_args = parser.parse_known_args()
log_dir = 'logs'

if not path.exists(log_dir):
    mkdir(log_dir, 0o755)

logging.basicConfig(
    level=logging.DEBUG if args.debug else logging.INFO,
    format='\t%(levelname)s(%(name)s) - %(asctime)s\t%(message)s',
    handlers=[
        logging.FileHandler(path.join(log_dir, strftime('%d-%m-%Y-%H-%M-%S.log'))),
        logging.StreamHandler(stdout)
    ]
)

logger = logging.getLogger(__file__)
