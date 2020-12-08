from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from typing import TypedDict




class User:
    
    class UserSettings(TypedDict):
        height_choice: str
        currency: str
        wage_period: str

    def __init__(self, user_settings:UserSettings):
        if user_settings != None:
            self.height = user_settings['height_choice']
            self.currency = user_settings['currency']
            self.wage_period = user_settings['wage_period']
        else:
            self.height = None
            self.currency = None
            self.wage_period = None
    
    @staticmethod
    def parseHtml(filepath: str) -> pd.DataFrame:
        now = time.time()
        with open(filepath, 'r') as f:
            soup = bs(f)
        table = soup.find('table')
        rows = list()
        for row in table.find_all('tr'):
            cols = [td.get_text(strip=True) for td in row.find_all('td')]
            rows.append(cols)
        later = time.time()
        headers = [td.get_text(strip=True) for td in table.find_all('th')]
        df = pd.DataFrame(rows[1:], columns=headers)
        print(len(df.columns))
        return df


User.parseHtml('S1.html')
