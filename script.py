import bs4
import requests
from getpass import getpass

TRIGGER_URL = 'http://192.168.1.1/'

AUTH_URL = 'http://172.16.1.11:1000/fgtauth?'

def init():
    pass

def login():
    
    ID = input("Enter your ID:")
    
    PASSWORD = getpass("Enter the password:")
     
    res = requests.get(TRIGGER_URL)
    
    soup = bs4.BeautifulSoup(res.content, 'html5lib')

    login_data = {
            'username' : ID,
            'password' : PASSWORD,
        }
    
    login_data['magic'] = soup.find('input', attrs={'name':'magic'})['value']
    
    _AUTH_URL = AUTH_URL + login_data['magic']
    
    # print(_AUTH_URL)
    
    with requests.Session() as ses:
        
        headers = {
                'user-agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
             }
        
        res = ses.post(_AUTH_URL, data=login_data, headers=headers)
        
        print('Successfully logged in!')

        KEEPALIVE

if __name__ == '__main__':
    login()
