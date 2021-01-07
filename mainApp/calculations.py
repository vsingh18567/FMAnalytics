import pandas as pd
from .models import Save, Player, Season, PlayerSeason

def calculate_season_positions(save: Save):
    '''
    Generates data for the seasons chart
    '''
    seasons = save.season_set.all()
    divisions = {}
    print(seasons)
    for season in seasons:
        divisions.update({season.division : season.teams_in_league})
    total_teams = 0
    division_pos = {}
    tickvals = []
    ticktext = []
    for key in sorted(divisions, reverse=True):
        division_pos.update({key: total_teams})
        total_teams += divisions[key]
        tickvals.append(total_teams)
        ticktext.append(f'Div {key}')
    season_positions = {'seasons': [], 'ys': [], 'labels': [], 'ticktext': ticktext, 'tickvals': tickvals}
    num_to_word = {1: '1st', 2: '2nd', 3: '3rd'}
    for season in seasons:
        boost = division_pos[season.division]
        true_y = divisions[season.division] - season.position + boost
        if season.position <= 3:
            label = f'Div {season.division}, {num_to_word[season.position]} place'
        else:
            label = f'Div {season.division}, {season.position}th place'
        season_positions['seasons'].append(season.end_year)
        season_positions['ys'].append(true_y)
        season_positions['labels'].append(label)
    
    if len(season_positions['seasons']) < 10:
        season_positions['seasons'] = [i + season_positions['seasons'][0] for i in range (0,10)]
    else:
        season_positions['seasons'] = season_positions['seasons'][-10:]

    json_data = {'max': total_teams, 'pos': season_positions}
    return json_data



def calculate_best_players(save : Save):
  '''
  Calculates the best defenders, creators and attackers
  '''
  save_players = save.player_set.all()
  df = pd.DataFrame(list(save_players.values()))
  df = df.loc[df['appearances'] > df['appearances'].median() * 0.75]
  normalise_cols = ['goals', 'goals_per_90', 'xG', 'shots_per_90', 'shot_percent',
                      'key_passes_per_90', 'pass_completion', 'dribbles_per_90', 'assists', 'assists_per_90',
                      'int_per_90', 'tackles_per_90', 'tackle_ratio', 'average_rating']
  for col in normalise_cols:
      df[col] = (df[col] - df[col].mean())/(df[col].std())
  
  df['defensive'] = (0.1 * df['average_rating'] + 0.3 * df['tackles_per_90'] + 0.15 * df['tackle_ratio'] + df['int_per_90'] * 0.3)
  df['creative'] = (0.1 * df['average_rating'] + 0.2 * df['assists_per_90'] + 0.15 * df['assists'] + df['key_passes_per_90'] * 0.3 + df['dribbles_per_90'] * 0.2 + df['pass_completion'] * 0.3)
  df['attacking'] = (0.1 * df['average_rating'] + df['goals'] * 0.1 + df['goals_per_90'] * 0.32 + df['xG'] * 0.12 + df['shots_per_90'] * 0.15 + df['shot_percent'] * 0.1)

  for col in ['defensive', 'creative', 'attacking']:
      df[col] = ((df[col] - df[col].mean())/(df[col].std()) + 1) * 50
  def_ = (list(df.nlargest(8, 'defensive')[['name', 'defensive']].values))
  cre_ = (list(df.nlargest(8, 'creative')[['name', 'creative']].values))
  att_ = list(df.nlargest(8, 'attacking')[['name', 'attacking']].values)
  for data in [def_, cre_, att_]:
      for i in range(len(data)):
          data[i] = data[i].tolist()

  return {'def': def_, 'cre': cre_, 'att': att_}


def get_years_played(player: Player) -> str:
    '''
    If a player has played in 2020-2021, 2021-2022, 2022-23, 2024-25, 2025-26 seasons, then this will return "2020-2023, 2024-26"
    '''
    playing_years = list()
    for s in player.playerseason_set.all():
        playing_years.append(s.season.end_year)
    playing_years.sort()
    index = 0
    ovr_str = ""
    while index < len(playing_years):
        start_yr = playing_years[index]
        cur_str = f'{start_yr-1}-'
        cur_year = playing_years[index]
        while index + 1 < len(playing_years) and playing_years[index+1] <= cur_year + 1:
            cur_year = playing_years[index+1]
            index += 1
        if start_yr == cur_year:
            cur_str = cur_str[:-1]
        else:
            cur_str += str(cur_year)
        index += 1
        ovr_str += cur_str
        ovr_str += ", "
    return ovr_str[:-2]