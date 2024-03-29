
import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action=argparse.BooleanOptionalAction,
                    default=False, type=bool, help='enable debug info')
args = parser.parse_args()

_format = '\t%(levelname)s(%(name)s) - %(asctime)s\t%(message)s'
logging.basicConfig(level=logging.DEBUG, format=_format) if args.debug else logging.basicConfig(level=logging.INFO, format=_format)
logger = logging.getLogger('')
