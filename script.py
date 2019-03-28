from __future__ import print_function
import bs4
import requests
from getpass import getpass
import time 
import sys
from configparser import ConfigParser

# TRIGGER_URL = 'http://192.168.1.1/'

# AUTH_URL = 'http://172.16.1.11:1000/fgtauth?'

KEEP_ALIVE_URL = 'http://172.16.1.11:1000/keepalive?05030309060a0423'

CONFIG_FILE = '.env'

TIMEOUT = 1000

class ConfigClass(object):

    def __init__(self, 
                USERNAME=None, 
                PASSWORD=None,
                TRIGGER_URL='http://192.168.1.1/',
                AUTH_URL='http://172.16.1.11:1000/fgtauth?'):

        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.TRIGGER_URL = TRIGGER_URL
        self.AUTH_URL = AUTH_URL

    def initConfig(self):

        try:
            configFile = open(CONFIG_FILE, 'r+')

            config = ConfigParser()

            config.read(CONFIG_FILE)
            
            try:
                
                self.USERNAME = config.get('USER_LOGIN', 'USERNAME')
                self.PASSWORD = config.get('USER_LOGIN', 'PASSWORD')

            except:

                raise
            
        except Exception:

            print('Login creadentials not found. Creating a new config file...')

            self.USERNAME = input("Enter your username/id : ")
            self.PASSWORD = getpass("Enter your password : ")

            config = ConfigParser()

            config['USER_LOGIN'] = {
                        'USERNAME': self.USERNAME, 
                        'PASSWORD': self.PASSWORD,
                        }

            with open(CONFIG_FILE, 'w') as configfile:
                config.write(configfile)

    def loginIntranet(self):
        
        res = requests.get(self.TRIGGER_URL)
        
        soup = bs4.BeautifulSoup(res.content, 'html5lib')

        login_data = {
                'username' : self.USERNAME,
                'password' : self.PASSWORD,
            }
        
        login_data['magic'] = soup.find('input', attrs={'name':'magic'})['value']
        
        _AUTH_URL = self.AUTH_URL + login_data['magic']
                
        with requests.Session() as ses:
            
            headers = {
                'connection':'keep-alive',
                'user-agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                }
            
            res = ses.post(_AUTH_URL, data=login_data, headers=headers)

            # print(res.next)

            soup = bs4.BeautifulSoup(res.content, 'html5lib')

            FAILED = soup.find('h1', attrs={'class':'logo'})
            
            if FAILED != None:

                FAILED = soup.find('h1', attrs={'class':'logo'}).text    

            if res.status_code == 200 and FAILED == 'Authentication Failed':
            
                print('Try logging again with correct password and username.')
            
            else:

                print('Successfully logged in!')

                while True:

                    for remaining in range(1000, 0, -1):
                        sys.stdout.write("\r")
                        sys.stdout.write("{:2d} seconds remaining.".format(remaining)) 
                        sys.stdout.flush()
                        time.sleep(1)

                    ses.get(KEEP_ALIVE_URL, headers=headers)

if __name__ == '__main__':
    conf = ConfigClass()
    conf.initConfig()
    conf.loginIntranet()
