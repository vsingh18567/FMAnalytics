import pandas as pd
from .models import Save, Player, Season, PlayerSeason
from django.db.models import Sum


def calculate_season_positions(save: Save):
    """
    Generates data for the seasons chart
    """
    seasons = save.season_set.all()
    if len(seasons) == 0:
        return None
    divisions = {}
    print(seasons)
    for season in seasons:
        divisions.update({season.division: season.teams_in_league})
    total_teams = 0
    division_pos = {}
    tickvals = []
    ticktext = []
    for key in sorted(divisions, reverse=True):
        division_pos.update({key: total_teams})
        total_teams += divisions[key]
        tickvals.append(total_teams)
        ticktext.append(f"Div {key}")
    season_positions = {
        "seasons": [],
        "ys": [],
        "labels": [],
        "ticktext": ticktext,
        "tickvals": tickvals,
    }
    num_to_word = {1: "1st", 2: "2nd", 3: "3rd"}
    for season in seasons:
        boost = division_pos[season.division]
        true_y = divisions[season.division] - season.position + boost
        if season.position <= 3:
            label = f"Div {season.division}, {num_to_word[season.position]} place"
        else:
            label = f"Div {season.division}, {season.position}th place"
        season_positions["seasons"].append(season.end_year)
        season_positions["ys"].append(true_y)
        season_positions["labels"].append(label)

    if len(season_positions["seasons"]) < 10:
        season_positions["seasons"] = [
            i + season_positions["seasons"][0] for i in range(0, 10)
        ]
    else:
        season_positions["seasons"] = season_positions["seasons"][-10:]

    json_data = {"max": total_teams, "pos": season_positions}
    return json_data


def calculate_best_players(qSet, identifier):
    """
    Calculates the best defenders, creators and attackers
    """
    df = pd.DataFrame(list(qSet.values()))
    df = df.loc[df["appearances"] > df["appearances"].median() * 0.75]
    normalise_cols = [
        "goals",
        "goals_per_90",
        "xG",
        "shots",
        "shot_percent",
        "key_passes",
        "pass_completion",
        "dribbles",
        "assists",
        "assists_per_90",
        "int_per_90",
        "tackles_per_90",
        "tackle_ratio",
        "average_rating",
    ]
    for col in normalise_cols:
        df[col] = (df[col] - df[col].mean()) / (df[col].std())

    df["defensive"] = (
        0.1 * df["average_rating"]
        + 0.3 * df["tackles_per_90"]
        + 0.15 * df["tackle_ratio"]
        + df["int_per_90"] * 0.3
    )
    df["creative"] = (
        0.1 * df["average_rating"]
        + 0.2 * df["assists_per_90"]
        + 0.15 * df["assists"]
        + df["key_passes"] * 0.3
        + df["dribbles"] * 0.2
        + df["pass_completion"] * 0.3
    )
    df["attacking"] = (
        0.1 * df["average_rating"]
        + df["goals"] * 0.1
        + df["goals_per_90"] * 0.32
        + df["xG"] * 0.12
        + df["shots"] * 0.15
        + df["shot_percent"] * 0.1
    )

    for col in ["defensive", "creative", "attacking"]:
        df[col] = ((df[col] - df[col].mean()) / (df[col].std()) + 1) * 50
    def_ = list(df.nlargest(8, "defensive")[[identifier, "defensive"]].values)
    cre_ = list(df.nlargest(8, "creative")[[identifier, "creative"]].values)
    att_ = list(df.nlargest(8, "attacking")[[identifier, "attacking"]].values)
    for data in [def_, cre_, att_]:
        for i in range(len(data)):
            data[i] = data[i].tolist()

    return {"def": def_, "cre": cre_, "att": att_}


def calculate_best_players2(qSet, identifier):
    """
    Calculates the best defenders, creators and attackers
    """
    df = pd.DataFrame(list(qSet.values()))
    if len(df) == 0:
        return None
    df = df.loc[df["appearances"] > df["appearances"].median() * 0.75]
    normalise_cols = [
        "goals",
        "goals_per_90",
        "xG",
        "shots_per_90",
        "shot_percent",
        "key_passes_per_90",
        "pass_completion",
        "dribbles_per_90",
        "assists",
        "assists_per_90",
        "int_per_90",
        "tackles_per_90",
        "tackle_ratio",
        "average_rating",
    ]
    for col in normalise_cols:
        df[col] = (df[col] - df[col].mean()) / (df[col].std())

    df["defensive"] = (
        0.1 * df["average_rating"]
        + 0.3 * df["tackles_per_90"]
        + 0.15 * df["tackle_ratio"]
        + df["int_per_90"] * 0.3
    )
    df["creative"] = (
        0.1 * df["average_rating"]
        + 0.2 * df["assists_per_90"]
        + 0.15 * df["assists"]
        + df["key_passes_per_90"] * 0.3
        + df["dribbles_per_90"] * 0.2
        + df["pass_completion"] * 0.3
    )
    df["attacking"] = (
        0.1 * df["average_rating"]
        + df["goals"] * 0.1
        + df["goals_per_90"] * 0.32
        + df["xG"] * 0.12
        + df["shots_per_90"] * 0.15
        + df["shot_percent"] * 0.1
    )

    for col in ["defensive", "creative", "attacking"]:
        df[col] = ((df[col] - df[col].mean()) / (df[col].std()) + 1) * 50
    def_ = list(df.nlargest(8, "defensive")[[identifier, "defensive"]].values)
    cre_ = list(df.nlargest(8, "creative")[[identifier, "creative"]].values)
    att_ = list(df.nlargest(8, "attacking")[[identifier, "attacking"]].values)
    for data in [def_, cre_, att_]:
        for i in range(len(data)):
            data[i] = data[i].tolist()

    return {"def": def_, "cre": cre_, "att": att_}


def get_years_played(player: Player) -> str:
    """
    If a player has played in 2020-2021, 2021-2022, 2022-23, 2024-25, 2025-26 seasons, then this will return
    "2020-2023, 2024-26"
    """
    playing_years = list()
    for s in player.playerseason_set.all():
        playing_years.append(s.season.end_year)
    playing_years.sort()
    index = 0
    ovr_str = ""
    while index < len(playing_years):
        start_yr = playing_years[index]
        cur_str = f"{start_yr - 1}-"
        cur_year = playing_years[index]
        while (
            index + 1 < len(playing_years) and playing_years[index + 1] <= cur_year + 1
        ):
            cur_year = playing_years[index + 1]
            index += 1
        if start_yr == cur_year:
            cur_str = cur_str[:-1]
        else:
            cur_str += str(cur_year)
        index += 1
        ovr_str += cur_str
        ovr_str += ", "
    return ovr_str[:-2]


def delete_season(season: Season) -> None:
    def calculate_division(calculation, default=0):
        try:
            return calculation()
        except:
            return default

    pseasons: list(PlayerSeason) = season.playerseason_set.all()
    for pseason in pseasons:
        player: Player = pseason.player
        player.seasons -= 1
        if player.seasons == 0:
            player.delete()
        else:
            player.appearances -= pseason.appearances
            player.minutes -= pseason.minutes
            player.goals -= pseason.goals
            player.assists -= pseason.assists
            player.reds -= pseason.reds
            player.yellows -= pseason.yellows
            player.xG -= pseason.xG
            player.pom -= pseason.pom
            player.cr_c -= pseason.cr_c
            player.minutes_per_season = player.minutes / player.seasons
            player.goals_per_xG = calculate_division(lambda: player.goals / player.xG)
            player.goals_per_90 = calculate_division(
                lambda: 90 * player.goals / player.minutes
            )
            player.assists_per_90 = calculate_division(
                lambda: 90 * player.assists / player.minutes
            )
            player.goals_per_xG = calculate_division(lambda: player.goals / player.xG)
            pseason.delete()
            player.determination, player.teamwork, player.leadership = (0, 0, 0)
            player.header_percent = 0
            player.average_rating = 0
            player.tackles_per_90 = 0
            player.tackle_ratio = 0
            player.int_per_90 = 0
            player.dribbles_per_90 = 0
            player.pass_completion = 0
            player.key_passes_per_90 = 0
            player.cr_c = 0
            player.shots_per_90 = 0
            player.shot_percent = 0
            player.max_value = 0
            new_pseasons = player.playerseason_set.all()
            for ps in new_pseasons:
                season_ratio = ps.minutes / player.minutes
                player.determination = ps.determination
                player.teamwork = ps.teamwork
                player.leadership = ps.leadership
                player.header_percent += ps.header_percent * season_ratio
                player.average_rating += ps.average_rating * season_ratio
                player.tackles_per_90 += ps.tackles_per_90 * season_ratio
                player.tackle_ratio += ps.tackle_ratio * season_ratio
                player.int_per_90 += ps.int_per_90 * season_ratio
                player.dribbles_per_90 += (90 * ps.dribbles / ps.minutes) * season_ratio
                player.pass_completion += ps.pass_completion * season_ratio
                player.key_passes_per_90 += (
                    90 * ps.key_passes / ps.minutes
                ) * season_ratio
                player.cr_c += ps.cr_c
                player.shots_per_90 += (90 * ps.shots / ps.minutes) * season_ratio
                player.shot_percent += ps.shot_percent * season_ratio
                player.max_value = max(player.max_value, ps.value)
            player.save()
