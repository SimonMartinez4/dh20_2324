# import packages
import sqlite3
import pandas as pd

# NBA api endpoints
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.endpoints import leaguehustlestatsplayer
from nba_api.stats.endpoints import leaguedashptdefend
from nba_api.stats.endpoints import leaguedashptstats

# extract xls
def extract_xls():
    ids = pd.read_excel('src/dh20_ids.xlsx', sheet_name='Feuil1')
    return ids

# transform 'player_id' in list
def list_dh20(ids):
    return ids['player_id'].tolist()

# extract stats via nba_api
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

# extract dfense via nba_api
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

# extract hustle via nba_api
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

# extract rebound via nba_api
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

# load with sqlite3
def load_data_to_db(df, table_name, db_path='dh20_stats.db'):
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

# extract all stats and load with load_data_to_db func
def extract_and_load_all_stats(player_ids, ids_df, db_path='dh20_stats.db'):

    adv_stats_reg = extract_player_stats(player_ids, season_type='Regular Season', measure_type='Advanced')
    load_data_to_db(adv_stats_reg, 'adv_stats_reg', db_path)
    
    adv_stats_po = extract_player_stats(player_ids, season_type='Playoffs', measure_type='Advanced')
    load_data_to_db(adv_stats_po, 'adv_stats_po', db_path)

    scor_stats_reg = extract_player_stats(player_ids, season_type='Regular Season', measure_type='Scoring')
    load_data_to_db(scor_stats_reg, 'scor_stats_reg', db_path)
    
    scor_stats_po = extract_player_stats(player_ids, season_type='Playoffs', measure_type='Scoring')
    load_data_to_db(scor_stats_po, 'scor_stats_po', db_path)
    
    base_stats_reg = extract_player_stats(player_ids, season_type='Regular Season', measure_type='Base')
    load_data_to_db(base_stats_reg, 'base_stats_reg', db_path)
    
    base_stats_po = extract_player_stats(player_ids, season_type='Playoffs', measure_type='Base')
    load_data_to_db(base_stats_po, 'base_stats_po', db_path)
    
    shot_def_reg = extract_defense_stats(player_ids, season_type='Regular Season')
    load_data_to_db(shot_def_reg, 'shot_def_reg', db_path)
    
    shot_def_po = extract_defense_stats(player_ids, season_type='Playoffs')
    load_data_to_db(shot_def_po, 'shot_def_po', db_path)
    
    hus_stats_reg = extract_hustle_stats(player_ids, season_type='Regular Season')
    load_data_to_db(hus_stats_reg, 'hus_stats_reg', db_path)
    
    hus_stats_po = extract_hustle_stats(player_ids, season_type='Playoffs')
    load_data_to_db(hus_stats_po, 'hus_stats_po', db_path)
    
    reb_reg = extract_rebound_stats(player_ids, season_type='Regular Season')
    load_data_to_db(reb_reg, 'reb_reg', db_path)
    
    reb_po = extract_rebound_stats(player_ids, season_type='Playoffs')
    load_data_to_db(reb_po, 'reb_po', db_path)
    
    load_data_to_db(ids_df, 'ids', db_path)

if __name__ == "__main__":
    ids_df = extract_xls()
    player_ids = list_dh20(ids_df)
    extract_and_load_all_stats(player_ids, ids_df)