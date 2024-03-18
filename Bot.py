import platform
from selenium import webdriver
import json
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep, time
import random
import re
import subprocess
import os
import requests
from atexit import register

max_time = 10

def open_chrome(port=9220, on_mac=True, on_linux=True):
    my_env = os.environ.copy()
    if platform.system() == 'Darwin' and on_mac:
        print('opening chrome (Mac)')
        subprocess.Popen(['open', '-a', "Google Chrome", '--args',
                         f'--remote-debugging-port={port}', 'https://www.example.com'])
    elif platform.system() == 'Linux' and on_linux:
        print('opening chrome (Linux)')
        subprocess.Popen(['google-chrome', f'--remote-debugging-port={port}', '--user-data-dir=data_dir'], env=my_env)
    else:
        print('opening chrome (Windows)')
        subprocess.Popen([r'C:\Program Files\Google\Chrome\Application\chrome.exe', f'--remote-debugging-port={port}', '--user-data-dir=data_dir'], env=my_env)
    print('opened chrome')

class Bot():
    def __init__(self, port_no=9220, headless=False, verbose=False):
        print('initialising bot')
        
        options = Options()
        if headless:
            options.add_argument("--headless")
        else:
            open_chrome()
            # attach to the same port that you're running chrome on options.add_experimental_option
            options.add_experimental_option(
                f"debuggerAddress", f"127.0.0.1: {port_no}")
        # without this, the chrome webdriver can't start (SECURITY RISK)
        options.add_argument("-no-sandbox")
        # options.add_argument("-window-size=1920x1080")
        self.driver = webdriver.Chrome(options=options) # create webdriver
        self.verbose = verbose
        
    def scroll(self, x=0, y=10000):
        self.driver.execute_script(f'window.scrollBy({x}, {y})')
        
    def click_btn(self, text):
        if self.verbose:
            print(f'clicking (text) btn')
        element_types = ['button', 'div', 'input', 'a', 'label']
        for element_type in element_types:
            btns = self.driver.find_elements_by_xpath(f'//{element_type}')
            
            try:
                btn = [b for b in btns if b.text.lower() == text.lower()][0]
                btn.click()
                return
            except IndexError:
                pass
            
            try:
                btn = self.driver.find_elements_by_xpath( 
                    f'//{element_type} [@value="{text}"]')[0]
                btn.click()
                return
            except:
                continue
            
        raise ValueError(f'button containing "{text}" not found')
    
    def _search(self, query, _type='search', placeholder=None):
        sleep (1)
        s = self.driver.find_elements_by_xpath(f'//input[@type="{_type}"]')
        print(s)
        if placeholder:
            s = [i for i in s if i.get_attribute( 
                'placeholder').lower() == placeholder.lower()] [0]
        else:
            s = s[0]
        s.send_keys(query)
    
    def toggle_verbose(self):
        self.verbose = not self.verbose
    
    def download_file(self, src_url, local_destination): 
        response = requests.get(src_url) 
        with open(local_destination, 'wb+') as f: 
            f.write(response.content)
    
    def s3_upload(self, obj, filename): 
        s3 = boto3.resource('s3') 
        s3.Object(key=filename).put(Body=json.dumps(obj))
    
    def _exit__(self, exc_type, exc_value, traceback): 
        self.driver.quit()
        

if __name__ == '__main__':
    bot = Bot()





        