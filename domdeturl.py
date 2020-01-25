'''
Class to determine desktop and mobile URL for given domain
'''

import logging
import requests

class DomDetURL:
    """
    Class to determine desktop and mobile URL for given domain
    """
    # Definition of an user agent string of an desktop browser
    ua_desktop = 'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)'
    # Definition of an user agent string of an mobile browser
    ua_mobile = 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 Build/KOT49H)'

    def __init__(self):
        logging.debug('init')
        # Disable logging messages of requests and urllib3
        logging.getLogger('requests').setLevel(logging.CRITICAL)
        logging.getLogger('urllib3').setLevel(logging.CRITICAL)

    def checkdomain(self, domain):
        """
        Method to determine desktop and mobile URL for given domain
        """
        logging.debug('domain [{}]'.format(domain))

        # Determine URL for desktop. Because of domain, dumb fake of base URL
        url_desktop = self.geturl(DomDetURL.ua_desktop, 'http://' + domain)
        logging.debug('url_desktop [{}]'.format(url_desktop))
        # Determine URL for mobile. Use desktop URL with mobile user agent
        url_mobile = self.geturl(DomDetURL.ua_mobile, 'http://' + domain)
        logging.debug('url_mobile [{}]'.format(url_mobile))

        # Return determined data
        return {'DOMAIN': domain, 'DESKTOP': url_desktop, 'MOBILE': url_mobile}

    def geturl(self, useragent, url_start):
        """
        Determine correct URL for given useragent.
        Asumption: Correct URL found when HTTP status code is 200
        """
        logging.debug('useragent [{}]'.format(useragent))
        logging.debug('url_start [{}]'.format(url_start))
        headers = {'User-Agent': useragent, }
        url_work = url_start

        # Loop until HTTP status code 200 reached
        while True:
            try:
                response = requests.head(url_work, headers=headers)
                if response.status_code == 200:
                    # HTTP status code 200 signals abort
                    break
                url_work = response.headers['Location']
                logging.debug('response.status_code [{}], new location [{}]'.format(response.status_code, url_work))
            except requests.exceptions.HTTPError as e:
                logging.info('HTTP error for [{}]: [{}]'.format(url_work, str(e)))
                break
            except requests.exceptions.ConnectionError as e:
                logging.info('Connection error for [{}]: [{}]'.format(url_work, str(e)))
                break
        return url_work
