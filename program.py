'''Script to figure out correct desktop and mobile URL for given domain
'''

from domdeturl import DomDetURL
import logging
import sys

# Configure logger
logging.basicConfig(
    filename='program.log',
    level=logging.INFO,
    filemode='w',
    format='%(asctime)s | %(levelname)s | %(funcName)s | %(message)s'
)

# Determine desktop and mobile url for passed domain
if __name__ == '__main__':
    logging.info('startup')
    min_domain = 1
    max_domain = len(sys.argv)
    if len(sys.argv) >= min_domain:
        obj = DomDetURL()
        while (min_domain < max_domain):
            domains = obj.checkdomain(sys.argv[min_domain])
            logging.info('domains [{}]'.format(domains))
            min_domain = min_domain + 1
