import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats, leaguehustlestatsplayer, leaguedashptdefend, leaguedashptstats

def extract_xls():
    ids = pd.read_excel('dh20_ids.xlsx', sheet_name='Feuil1')
    return ids

def list_dh20(ids):
    return ids['player_id'].tolist()

def extract_player_stats(player_ids, season='2023-24', season_type='Regular Season', measure_type="Base", per_mode="PerGame"):
    try:
        stats = leaguedashplayerstats.LeagueDashPlayerStats(
            season=season,
            season_type_all_star=season_type,
            per_mode_detailed=per_mode,
            measure_type_detailed_defense=measure_type
        )
        df = stats.get_data_frames()[0]
        df_filtered = df[df['PLAYER_ID'].isin(player_ids)]
        return df_filtered
    except Exception as e:
        print(f"Erreur lors de l'extraction des données de player stats: {e}")
        return None

def extract_defense_stats(player_ids, season='2023-24', season_type='Regular Season'):
    try:
        stats = leaguedashptdefend.LeagueDashPtDefend(
            season=season,
            season_type_all_star=season_type,
            defense_category="Overall",
            per_mode_simple="PerGame",
            league_id="00"
        )
        df = stats.get_data_frames()[0]
        df_filtered = df[df['CLOSE_DEF_PERSON_ID'].isin(player_ids)]
        return df_filtered
    except Exception as e:
        print(f"Erreur lors de l'extraction des données de defense stats: {e}")
        return None

def extract_hustle_stats(player_ids, season='2023-24', season_type='Regular Season'):
    try:
        stats = leaguehustlestatsplayer.LeagueHustleStatsPlayer(
            season=season,
            season_type_all_star=season_type,
            per_mode_time="PerGame"
        )
        df = stats.get_data_frames()[0]
        df_filtered = df[df['PLAYER_ID'].isin(player_ids)]
        return df_filtered
    except Exception as e:
        print(f"Erreur lors de l'extraction des données de hustle stats: {e}")
        return None

def extract_rebound_stats(player_ids, season='2023-24', season_type='Regular Season'):
    try:
        stats = leaguedashptstats.LeagueDashPtStats(
            season=season,
            season_type_all_star=season_type,
            player_or_team="Player",
            pt_measure_type="Rebounding",
            per_mode_simple="PerGame"
        )
        df = stats.get_data_frames()[0]
        df_filtered = df[df['PLAYER_ID'].isin(player_ids)]
        return df_filtered
    except Exception as e:
        print(f"Erreur lors de l'extraction des données de rebound stats: {e}")
        return None

def load_data_to_csv(df, file_name):
    try:
        df.to_csv(f'{file_name}.csv', index=False)
        print(f"Data loaded into {file_name}.csv successfully.")
    except Exception as e:
        print(f"Error loading data to csv: {e}")

def extract_and_load_all_stats(player_ids, ids_df):
    adv_stats_reg = extract_player_stats(player_ids, season_type='Regular Season', measure_type='Advanced')
    if adv_stats_reg is not None:
        load_data_to_csv(adv_stats_reg, 'adv_stats_reg')
    
    adv_stats_po = extract_player_stats(player_ids, season_type='Playoffs', measure_type='Advanced')
    if adv_stats_po is not None:
        load_data_to_csv(adv_stats_po, 'adv_stats_po')

    scor_stats_reg = extract_player_stats(player_ids, season_type='Regular Season', measure_type='Scoring')
    if scor_stats_reg is not None:
        load_data_to_csv(scor_stats_reg, 'scor_stats_reg')
    
    scor_stats_po = extract_player_stats(player_ids, season_type='Playoffs', measure_type='Scoring')
    if scor_stats_po is not None:
        load_data_to_csv(scor_stats_po, 'scor_stats_po')
    
    base_stats_reg = extract_player_stats(player_ids, season_type='Regular Season', measure_type='Base')
    if base_stats_reg is not None:
        load_data_to_csv(base_stats_reg, 'base_stats_reg')
    
    base_stats_po = extract_player_stats(player_ids, season_type='Playoffs', measure_type='Base')
    if base_stats_po is not None:
        load_data_to_csv(base_stats_po, 'base_stats_po')
    
    shot_def_reg = extract_defense_stats(player_ids, season_type='Regular Season')
    if shot_def_reg is not None:
        load_data_to_csv(shot_def_reg, 'shot_def_reg')
    
    shot_def_po = extract_defense_stats(player_ids, season_type='Playoffs')
    if shot_def_po is not None:
        load_data_to_csv(shot_def_po, 'shot_def_po')
    
    hus_stats_reg = extract_hustle_stats(player_ids, season_type='Regular Season')
    if hus_stats_reg is not None:
        load_data_to_csv(hus_stats_reg, 'hus_stats_reg')
    
    hus_stats_po = extract_hustle_stats(player_ids, season_type='Playoffs')
    if hus_stats_po is not None:
        load_data_to_csv(hus_stats_po, 'hus_stats_po')
    
    reb_reg = extract_rebound_stats(player_ids, season_type='Regular Season')
    if reb_reg is not None:
        load_data_to_csv(reb_reg, 'reb_reg')
    
    reb_po = extract_rebound_stats(player_ids, season_type='Playoffs')
    if reb_po is not None:
        load_data_to_csv(reb_po, 'reb_po')
    
    load_data_to_csv(ids_df, 'ids')

if __name__ == "__main__":
    ids_df = extract_xls()
    player_ids = list_dh20(ids_df)
    extract_and_load_all_stats(player_ids, ids_df)