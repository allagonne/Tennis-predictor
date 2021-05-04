from datetime import datetime,timedelta

from past_attributes import *
from elo_attributes import *
from categorical_attributes import *
#from stategy_assessment import *

import os.path as path
import glob

one_up = path.abspath(path.join(__file__ ,".."))
two_up =  path.abspath(path.join(__file__ ,"../.."))
three_up =  path.abspath(path.join(__file__ ,"../../.."))
print()
#remember to pip3 install --upgrade pip before 'pip install -r requirements.txt'


################################################################################
######################### Building of the raw dataset ##########################
################################################################################

## Dataset presentation (Jeff Sackman tennis_ATP matches)

path = three_up + '/Data/atp_matches*.csv'
filenames=list(glob.glob(path))
dfs = []
for filename in filenames:
    dfs.append(pd.read_csv(filename))
## Concatenate all data into one DataFrame
big_frame = pd.concat(dfs, ignore_index=True)

## Cleaning of NAN values in 'loser_hand'
big_frame = big_frame.dropna(axis=0, subset=['loser_hand', 'winner_hand', 'surface'])
big_frame = big_frame[~big_frame['surface'].isin(['Carpet'])]
big_frame = big_frame[~big_frame['round'].isin(['BR'])]
big_frame = big_frame[~big_frame['draw_size'].isin([16])]
big_frame = big_frame[~big_frame['draw_size'].isin([12])]
big_frame = big_frame.reset_index(drop=True)

## Tourney_date type configuration
big_frame['tourney_date'] = pd.to_datetime(big_frame['tourney_date'], format='%Y%m%d')
big_frame = big_frame.sort_values(['tourney_date', 'match_num'])
big_frame = big_frame.reset_index(drop=True)

## Seperate Sets/Games


################################################################################
############################ Adding Relevant Values ############################
################################################################################


## Adding ELO to each row
elo_rankings = compute_elo_rankings(big_frame)
big_frame = pd.concat([big_frame,elo_rankings],1)


## Selecting Period we are interested in

df = big_frame
beg = datetime.datetime(2011,1,1) 
end = df.tourney_date.iloc[-1]
indices = df[(df.tourney_date>beg)&(df.tourney_date<=end)].index

#os._exit(0)

## Building of attributes based on the past matches

features_player  = features_past_generation(120,360,df,indices)
features_player.to_csv(three_up + "/Data/Generated csv/features_player.csv",index=False)

################################################################################
############################ Final dataset selection ###########################
################################################################################


#selection of our period dataset

df_selected = df.iloc[indices,:].reset_index(drop=True)
df_selected.shape



# Categorical data

#Categorical_data = df_selected[["surface","draw_size","winner_hand","winner_ioc","loser_hand","loser_ioc","best_of","round"]]
''' Pree cleaning:
surface: 3 cat columns
draw_size: 6 cat columns
winner_hand: 3 cat columns
winner_ioc: 71 cat columns
loser_ioc: 82 cat columns
loser_hand: 3 cat columns
best_of: 2 cat colimns
round: 8 cat features
'''

#categorical_data = df_selected[["surface","draw_size","best_of","round"]] + features_player[["player1_hand", "player2_hand"]]
#cat_table = categorical_features_encoding(categorical_data)
categorical_data = pd.concat([df_selected[["surface","draw_size","best_of","round"]],features_player[["player1_hand", "player2_hand"]]],1)
#categorical_data.to_csv(three_up + "/Data/Generated csv/categorical_data.csv",index=False)
#column = categorical_data["surface"]
#print
#column.value_counts()


cat_table = categorical_features_encoding(categorical_data)
features_player.drop(['player1_hand','player2_hand'], inplace=True, axis=1)

# Final Concatenation
ml_data = pd.concat([features_player, cat_table],1)

# Re-order columns
ml_data = ml_data[['player1_name',
                    'player1_age',
                    'player1_height',
                    'player1_ranking_points',
                    'player1_elo',
                    'player1_hand_1',
                    'player1_hand_2',
                    'player1_wins',
                    'player1_losses',
                    'player1_total_games',
                    'player1_W/total_games',
                    'player1_Wins_per_surface',
                    'player1_Losses_per_surface',
                    'player1_total_games_per_surface',
                    'player1_W/total_games_per_surface',
                    'player1_won_h2h',
                    'player2_name',
                    'player2_age',
                    'player2_height',
                    'player2_ranking_points',
                    'player2_elo',
                    'player2_hand_1',
                    'player2_hand_2',
                    'player2_wins',
                    'player2_losses',
                    'player2_total_games',
                    'player2_W/total_games',
                    'player2_Wins_per_surface',
                    'player2_Losses_per_surface',
                    'player2_total_games_per_surface',
                    'player2_W/total_games_per_surface',
                    'player2_won_h2h',
                    'games_h2h',
                    'player1_winrate',
                    'surface_1',
                    'surface_2',
                    'draw_size_1',
                    'draw_size_2',
                    'draw_size_3',
                    'draw_size_4',
                    'draw_size_5',
                    'draw_size_6',
                    'draw_size_7',
                    'draw_size_8',
                    'draw_size_9',
                    'best_of_3',
                    'round_1',
                    'round_2',
                    'round_3',
                    'round_4',
                    'round_5',
                    'round_6',
                    'round_7',
                    'outcome'
                    ]]

ml_data.to_csv(three_up + "/Data/Generated csv/atp_data_attributes.csv",index=False)
