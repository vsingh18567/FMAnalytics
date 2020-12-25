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

    def __init__(self, file, save: Save, season: Season, user_settings:UserSettings):
        self.save = save
        self.file = file
        self.season = season
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
    

    def parse_html(self) -> pd.DataFrame:
        soup = bs(self.file, features="html.parser")
        table = soup.find('table')
        rows = list()
        for row in table.find_all('tr'):
            cols = [td.get_text(strip=True) for td in row.find_all('td')]
            rows.append(cols)
        headers = [td.get_text(strip=True) for td in table.find_all('th')]
        df = pd.DataFrame(rows[1:], columns=headers)
        return df

    def get_player(self, row : pd.Series) -> Player:
        named_players = Player.objects.filter(name=row['Name'])
        for player in named_players:
            if player.game_save == self.save:
                return player

        player = Player(
                game_save = self.save,
                name = row['Name'],
                nationality = row['Nat'],
                seasons = 0,
                appearances = 0,
                goals = 0,
                assists = 0,
                average_rating = 0,
                pom = 0,
                reds = 0,
                yellows = 0,
                best_role = row['Best Role'],
                max_value = 0,
                home_grown_status = len(row['Home-Grown Status']) > 2
                )
        player.save()
        return player
    
    def add_data(self, player : Player, row : pd.Series) -> None:
        # Step 1: Create Player Season
        def extract_wage(string: str) -> int:
            '''
            typical value: "$350,000 p/w"
            '''
            num_str = ""
            for char in string:
                if char.isnumeric():
                    num_str += char
            if len(num_str) == 0:
                return 0
            else:
                return int(num_str)
        
        def extract_value(string: str) -> int:
            '''
            typical value: "$57.3M"
            '''
            denomination = 1
            num_str = ""
            for char in string:
                if char.isnumeric():
                    num_str += char
                elif char == "." or char == ",":
                    num_str += "."
            if string[-1] == "M" or string[-1] == "m":
                denomination = 10**6
            elif string[-1] == "K" or string[-1] == "k":
                denomination = 10**3
            if len(num_str) == 0:
                return 0
            num = float(num_str)
            return num * denomination

        def extract_appearances(string: str) -> int:
            '''
            typical value:
            '''
            num_str = ""
            for char in string:
                if char.isnumeric():
                    num_str += char
                else:
                    break
            if len(num_str) == 0:
                return 0
            return int(num_str)

        def extract_cs(string: str) -> int:
            if string.isnumeric():
                return int(string)
            else:
                return 0

        def extract_dist(string: str) -> int:
            num_str = ""
            for char in string:
                if char.isnumeric() or char == ".":
                    num_str += char
                elif char == ",":
                    num_str += "."
            if len(num_str) == 0:
                return 0
            return float(num_str)

        player_season = PlayerSeason(
            season = self.season,
            player = player,
            best_role = row['Best Role'],
            age = int(row['Age']),
            wage = extract_wage(row['Wage']),
            playing_time = row['Actual Playing Time'],
            value = extract_value(row['Value']),
            determination = int(row['Det']),
            teamwork = int(row['Tea']),
            leadership = int(row['Ldr']),
            appearances = extract_appearances(row['Apps']),
            minutes = extract_wage(row['Mins']),
            average_rating = extract_value(row['Av Rat']),
            pom = int(row['PoM']),
            goals = int(row['Gls']),
            assists = int(row['Ast']),
            reds = int(row['Red']),
            yellows = int(row['Yel']),
            clean_sheets = extract_cs(row['Clean sheets']),
            conceded = extract_cs(row['Conc']),
            goal_mistakes = int(row['Gl Mst']),
            header_percent = extract_wage(row['Hdr %']),
            int_per_90 = extract_value(row['Int/90']),
            tackles = extract_value(row['Tck']),
            tackle_ratio = extract_wage(row['Tck R']),
            cr_c = extract_cs(row['Cr C']),
            dist_per_90 = extract_dist(row['Dist/90']),
            dribbles = int(row['Drb']),
            pass_completion = extract_wage(row['Pas %']),
            key_passes = int(row['K Pas']),
            penalties = int(row['Pens']),
            xG = float(row['xG']),
            shots = int(row['Shots']),
            shot_percent = extract_wage(row['Shot %'])
        )
        player_season.save()


        # Step 2: Update player data
        player.seasons += 1
        try:
            player.average_rating = (player.average_rating * player.appearances + player_season.average_rating * player_season.appearances) / (player.appearances + player_season.appearances)
        except:
            # divide by zero
            player.average_rating = 0
        player.appearances += player_season.appearances
        player.goals += player_season.goals
        player.assists += player_season.assists
        player.pom += player_season.pom
        player.reds += player_season.reds
        player.yellows += player_season.yellows
        player.best_role = player_season.best_role
        player.max_value = max(player_season.value, player.max_value)
        player.home_grown_status = len(row['Home-Grown Status']) > 2
        player.save()

    def _main(self):
        df : pd.DataFrame = self.parse_html()
        print(df.columns)
        for row in df.iterrows():
            player : Player = self.get_player(row[1])
            self.add_data(player, row[1])

