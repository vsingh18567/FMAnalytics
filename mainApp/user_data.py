from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from typing import TypedDict
from .models import Save, Player, Season, PlayerSeason



class UserData:
    
    class UserSettings(TypedDict):
        height_choice: str
        currency: str
        wage_period: str
        distance_choice: str

    def __init__(self, save: Save, user_settings:UserSettings):
        self.save = save
        if user_settings != None:
            self.height = user_settings['height_choice']
            self.currency = user_settings['currency']
            self.wage_period = user_settings['wage_period']
            self.distance_choice = user_settings['distance_choice']
        else:
            self.height = None
            self.currency = None
            self.wage_period = None
            self.distance_choice = None
    
    @staticmethod
    def parseHtml(file) -> pd.DataFrame:
        soup = bs(file, features="html.parser")
        table = soup.find('table')
        rows = list()
        for row in table.find_all('tr'):
            cols = [td.get_text(strip=True) for td in row.find_all('td')]
            rows.append(cols)
        headers = [td.get_text(strip=True) for td in table.find_all('th')]
        df = pd.DataFrame(rows[1:], columns=headers)
        print(df.columns)

    def add_player(row : pd.Series) -> None:
        if len(Player.objects.filter(name=row['Name'])) == 0:
            pass
    def _main(self):
        pass


